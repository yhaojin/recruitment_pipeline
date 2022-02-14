from django.shortcuts import render

from custom_user.models import User
from account.views import LoginView
from account.utils import default_redirect


class CustomLogInView(LoginView):

    def get_success_url(self, fallback_url=None, **kwargs):

        # if user is job seeker, then redirect page should be to jobs_portal
        # if user is recruiter, then redirect page should be to recruiter_portal
        if fallback_url is None:
            if self.request.user.category == User.JOB_SEEKER:
                fallback_url = 'jobs_portal'
            else:
                fallback_url = 'recruiter_portal'

        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)
