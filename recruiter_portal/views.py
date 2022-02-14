from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

from .models import Task

from job_applications.models import Job, Application
from custom_user.models import User

from typing import List


class RecruiterIndexView(LoginRequiredMixin, TemplateView):
    """
    Default view of the recruiter portal page, which is the page after a recruiter successfully signs in.
    Page should show all jobs available as well as jobs applications.
    """

    template_name = 'recruiter_portal/recruiter_main.html'

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        # No follow up actions necessary for HIRED and REJECTED applications.
        relevant_applications = list(Application.objects.select_related("job", "recruiter").filter(
            (~Q(stage=Application.HIRED) | Q(stage=Application.REJECTED)) &
            (Q(recruiter=None) | Q(recruiter=self.request.user))).order_by("pk"))

        unassigned_applications = []
        assigned_applications = []
        for application in relevant_applications:
            if not application.recruiter:
                unassigned_applications.append(application)
            else:
                assigned_applications.append(application)

        ctx.update({"unassigned_applications": unassigned_applications,
                    "assigned_applications": assigned_applications, })

        return ctx


def take_on_application_view(request: HttpRequest, application_pk: str):
    """
    View that allows the recruiter to take on the application under his charge.
    """

    if request.user.category != User.RECRUITER:
        return redirect('jobs_portal')

    application: Application = Application.objects.get_or_none(pk=application_pk)
    if not application:
        return redirect('recruiter_portal')

    application.recruiter = request.user
    application.save()

    tasks: List["Task"] = Task.objects.filter(application=application, is_completed=False)
    for task in tasks:
        task.recruiter = request.user
        task.save()

    return redirect('recruiter_portal')


class SaveTaskChangesView(View):

    def post(self, request, *args, **kwargs):

        task_pk = self.kwargs['task_pk']
        task: Task = Task.objects.get_or_none(pk=task_pk)
        if not task:
            return redirect("recruiter_portal")

        notes = request.POST.get("task-notes")
        complete_task = True if request.POST.get("complete-task") == "yes" else False

        task.notes = notes
        task.is_completed = complete_task
        task.save()

        return redirect("job_application", application_pk=task.application.pk)
