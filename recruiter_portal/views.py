from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class RecruiterIndexView(LoginRequiredMixin, TemplateView):
    """
    Default view of the recruiter portal page, which is the page after a recruiter successfully signs in.
    Page should show all jobs available as well as jobs applications.
    """

    template_name = 'recruiter_portal/recruiter_main.html'