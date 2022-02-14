from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

from .forms import ApplicationForm

from job_applications.models import Job, Application
from job_applications.utils import time_now_utc, create_deadline
from recruiter_portal.models import Task
from custom_user.models import User
from django.utils.encoding import smart_str

import os
from typing import List


class JobView(LoginRequiredMixin, FormView):
    """
    Job view. For job seeker this contains information of the job and the details to apply. For recruiters, this shows
    a list of all job applicants.
    """

    template_name = 'job/job.html'
    form_class = ApplicationForm
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('jobs_portal')

    def get_form_kwargs(self):

        kwargs = super(JobView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def form_valid(self, form):

        form.instance.user = self.request.user
        form.instance.email = self.request.POST.get("email")

        job = Job.objects.get(pk=self.kwargs['job_pk'])
        if not job.is_open:
            raise ValueError("Not able to apply for a job which is no longer open!")

        form.instance.job = job
        form.instance.stage = Application.PENDING

        application = form.save(commit=True)

        # create a task for the recruiter to follow up on
        time_now = time_now_utc()
        due_date = create_deadline(time=time_now, days=Application.STAGE_TO_TASKS[Application.PENDING]["deadline"])
        Task.objects.create(job=job, application=application,
                            description=Application.STAGE_TO_TASKS[Application.PENDING]["description"], due_date=due_date)

        return super(JobView, self).form_valid(form)

    def form_invalid(self, form):

        job = Job.objects.select_related("company").get(pk=self.kwargs['job_pk'])

        return self.render_to_response(self.get_context_data(job, form=form))

    def get(self, request, *args, **kwargs) -> HttpResponse:

        # do not allow closed jobs to be seen anymore
        job = Job.objects.select_related("company").get(pk=self.kwargs['job_pk'])
        if not job.is_open:
            return redirect("jobs_portal")

        context = self.get_context_data(job=job, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, job, **kwargs):

        ctx = super().get_context_data(**kwargs)

        ctx.update({"job": job})

        # Recruiter will be able to see the all applications
        if self.request.user.category == User.RECRUITER:

            applications = list(Application.objects.select_related("job", "recruiter").filter(job=job).order_by("pk"))
            ctx.update({"recruiter": True, "applications": applications})

        return ctx


class JobApplicationView(LoginRequiredMixin, TemplateView):
    """
    Job application view, contains information of the job and the details to apply.
    """

    template_name = 'portal/job_application.html'
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('jobs_portal')

    def get(self, request, *args, **kwargs) -> HttpResponse:

        application: Application = Application.objects.get_or_none(pk=self.kwargs['application_pk'])
        if not application:
            return redirect("jobs_portal")

        if not application.job.is_open:
            return redirect("jobs_portal")

        context = self.get_context_data(application=application, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, application, **kwargs):

        ctx = super().get_context_data(**kwargs)

        ctx.update({"job": application.job, "application": application})

        # Recruiter will be able to see the specific user's application.
        if self.request.user.category == User.RECRUITER:

            tasks: List["Task"] = Task.objects.filter(application=application,
                                                      recruiter=self.request.user,
                                                      is_completed=False)

            ctx.update({"recruiter": True,
                        "tasks": tasks,
                        "next_stages": application.possible_next_stages})

        return ctx


def change_application_stage(request: HttpRequest, application_pk):
    """
    View that changes the application's stage to the next stage
    """

    if request.user.category != User.RECRUITER:
        return redirect('jobs_portal')

    application = Application.objects.get_or_none(pk=application_pk)
    if not application:
        return redirect('recruiter_portal')

    category = int(request.POST.get("category"))
    if category not in Application.NEXT_STAGE[application.stage]:
        raise ValueError(f"Unable to move to stage {category} from {application.stage}")

    tasks: List["Task"] = Task.objects.filter(application=application, is_completed=False)
    if tasks:
        raise ValueError(f"Unable to move to next stage when there are outstanding tasks.")

    application.stage = category
    application.save()

    Task.proceed_to_next_task(application=application)

    return redirect('job_application', application_pk=application.pk)


def download_resume_view(request: HttpRequest, application_pk):
    """
    View that generates a downloadable link for the uploaded resume
    """

    application = Application.objects.get(pk=application_pk)
    response = HttpResponse(
        content_type='application/force-download')  # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(application.resume.path)

    response['X-Sendfile'] = smart_str(application.resume.path)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
