from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.core.files import File
from custom_user.models import User
from job_applications.utils import time_now_utc
from job_applications.models import Company, Application, Job
from job_applications.views import JobView, JobApplicationView, change_application_stage
from job_applications.forms import ApplicationForm

from recruiter_portal.models import Task

from .test_job_application_methods import JobsTestObject

from django.utils import timezone as tz

import math
import re
import os
from django.conf import settings


class JobApplicationViewTestCase(TestCase):

    def setUp(self):

        self.jobs_test_object = JobsTestObject()

    # def test_job_view(self):
    #     """
    #     Test case which tests that submission of job application on Job View results in correct behaviour.
    #     """
    #
    #     with open(os.path.join(os.path.join(settings.BASE_DIR, 'job_applications', 'tests'), 'empty_resume.pdf'), 'rb') as local_file:
    #         empty_resume = File(local_file)
    #
    #         # self.client = Client()
    #         # self.client.login(username=self.jobs_test_object.user1.username, password='pass@123')
    #         # self.content_type = "application/json"
    #         # response = self.client.post(reverse("job", kwargs={"job_pk": self.jobs_test_object.job_dbs_product_manager.pk}),
    #         #                             data={"resume": empty_resume}, content_type="multipart/form-data; boundary=something")
    #
    #         form = ApplicationForm(data={"resume": empty_resume,
    #                                      "email": self.jobs_test_object.user1.email,
    #                                      },
    #                                user=self.jobs_test_object.user1)
    #
    #         assert form.is_valid() is True
    #
    #         task_count = Task.objects.all().count()
    #         assert task_count == 0
    #
    #         request = RequestFactory().post('/')
    #         request.user = self.jobs_test_object.user1
    #         job_view = JobView()
    #         job_view.setup(request, **{'job_pk': self.jobs_test_object.job_google_full_stack.pk})
    #         job_view.form_valid(form=form)
    #
    #         task_count = Task.objects.filter(job=self.jobs_test_object.job_google_full_stack).count()
    #         assert task_count == 1
    #     # assert response.status_code == 200

    def test_job_application_view(self):
        """
        Test case which tests for Job Application View. Job Seeker and Recruiters should see different contexts.
        """

        # test that the correct contexts are given when a recruiter logs in
        request = RequestFactory().post('/')
        request.user = self.jobs_test_object.recruiter
        job_application_view = JobApplicationView()
        job_application_view.setup(request, **{'application_pk': self.jobs_test_object.application_pending.pk})

        ctx = job_application_view.get_context_data(application=self.jobs_test_object.application_pending)
        assert ctx["recruiter"] is True
        assert ctx["recruiter"] is True

    def test_change_application_stage_view(self):
        """
        Test case which tests that the application stage can be changed correctly
        """

        request = RequestFactory().post('/')
        request.POST = {"category": Application.REVIEWING}
        request.user = self.jobs_test_object.recruiter

        task = Task.objects.get_or_none(application=self.jobs_test_object.application_pending)
        assert task is None

        change_application_stage(request, application_pk=self.jobs_test_object.application_pending.pk)
        task = Task.objects.get_or_none(application=self.jobs_test_object.application_pending)
        assert task.description == Application.STAGE_TO_TASKS[Application.REVIEWING]["description"]









