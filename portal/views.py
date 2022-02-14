from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import ApplicationForm

from job_applications.models import Job, Application

# Create your views here.


class JobsIndexView(LoginRequiredMixin, FormView):
    """
    Default view of the portal page, which is the page after a user successfully signs in.
    Page should show all jobs available as well as jobs applied for.
    """

    template_name = 'portal/jobs_main.html'
    form_class = ApplicationForm
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('jobs_portal')

    def get_form_kwargs(self):

        kwargs = super(JobsIndexView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):

        form.instance.user = self.request.user

        form.instance.email = self.request.POST.get("email")

        job = Job.objects.get(pk=self.request.POST.get("job"))
        form.instance.job = job
        form.instance.stage = Application.PENDING

        form.save(commit=True)

        return super(JobsIndexView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        applications = list(Application.objects.select_related("job").filter(user=self.request.user))
        applied_jobs_pk = [application.job.pk for application in applications]

        open_jobs = list(Job.objects.select_related("company").filter(Q(is_open=True) & ~Q(pk__in=applied_jobs_pk)))

        ctx.update({"applications": applications,
                    "open_jobs": open_jobs})

        return ctx