from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

from .forms import ApplicationForm

from job_applications.models import Job, Application

import os
import magic


class JobsIndexView(LoginRequiredMixin, TemplateView):
    """
    Default view of the portal page, which is the page after a user successfully signs in.
    Page should show all jobs available as well as jobs applied for.
    """

    template_name = 'portal/jobs_main.html'
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('jobs_portal')

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        applications = list(Application.objects.select_related("job").filter(user=self.request.user))
        applied_jobs_pk = [application.job.pk for application in applications]

        open_jobs = list(Job.objects.select_related("company").filter(Q(is_open=True) & ~Q(pk__in=applied_jobs_pk)))

        ctx.update({"applications": applications,
                    "open_jobs": open_jobs})

        return ctx
