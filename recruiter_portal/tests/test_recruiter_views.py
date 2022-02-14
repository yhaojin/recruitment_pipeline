from django.test import TestCase, SimpleTestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.core.files import File
from custom_user.models import User
from job_applications.utils import time_now_utc
from job_applications.models import Application
from recruiter_portal.views import RecruiterIndexView, take_on_application_view, SaveTaskChangesView

from job_applications.tests.test_job_application_methods import JobsTestObject

from recruiter_portal.models import Task


from django.utils import timezone as tz

import math
import re
import json
import os
from django.conf import settings


class RecruiterViewsTestCase(TestCase):

    def setUp(self):
        self.jobs_test_object = JobsTestObject()

        # this is the only user who created an application that is not yet covered by any recruiter
        self.new_user = User.objects.create(
            username="new_user",
            email="new_user@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )

        with open(os.path.join(os.path.join(settings.BASE_DIR, 'job_applications', 'tests'), 'empty_resume.pdf'), 'rb') as local_file:
            self.empty_resume = File(local_file)

            self.new_application_pending = Application.objects.create(
                user=self.new_user, email=self.new_user.email,
                job=self.jobs_test_object.job_google_full_stack, stage=Application.PENDING, resume=self.empty_resume,
            )

            self.new_application_pending_task = Task.proceed_to_next_task(application=self.new_application_pending)

    def test_recruiter_index_view(self):
        """
        Test case which tests that there will be correct number of applications generated according to recruiter.
        """

        # test that the correct contexts are given when a recruiter logs in
        request = RequestFactory().post('/')
        request.user = self.jobs_test_object.recruiter
        recruit_index_view = RecruiterIndexView()
        recruit_index_view.setup(request)

        ctx = recruit_index_view.get_context_data()
        assert ctx["unassigned_applications"] == [self.new_application_pending]

        assert len(ctx["assigned_applications"]) == len([self.jobs_test_object.application_pending,
                                                         self.jobs_test_object.application_reviewing,
                                                         self.jobs_test_object.application_shortlisted,
                                                         self.jobs_test_object.application_interviewing])
        for application in ctx["assigned_applications"]:
            assert application in [self.jobs_test_object.application_pending,
                                   self.jobs_test_object.application_reviewing,
                                   self.jobs_test_object.application_shortlisted,
                                   self.jobs_test_object.application_interviewing]

    def test_take_on_application_view(self):
        """
        Test that when a recruiter takes on a case, all tasks will be transferred to him.
        """

        request = RequestFactory().post('/')
        request.user = self.jobs_test_object.recruiter

        # check that recruiter for application is correctly assigned.
        assert self.new_application_pending.recruiter is None
        assert self.new_application_pending_task.recruiter is None
        take_on_application_view(request, application_pk=self.new_application_pending.pk)
        self.new_application_pending.refresh_from_db()
        self.new_application_pending_task.refresh_from_db()
        assert self.new_application_pending.recruiter == self.jobs_test_object.recruiter
        # check that the tasks have been correctly transferred to recruiter
        assert self.new_application_pending_task.recruiter == self.jobs_test_object.recruiter

    def test_save_task_changes_view(self):
        """
        Test that when a recruiter saves task, the changes are saved correctly.
        """

        pending_task = Task.proceed_to_next_task(application=self.jobs_test_object.application_pending)
        assert pending_task.is_completed is False

        save_task_changes_view = SaveTaskChangesView(kwargs={'task_pk': pending_task.pk})
        request = RequestFactory().post('/')
        request.POST = {"task-notes": 'some notes', 'complete-task': "yes", }
        request.user = self.jobs_test_object.recruiter

        save_task_changes_view.post(request=request, kwargs={'task_pk': pending_task.pk})
        pending_task.refresh_from_db()
        assert pending_task.is_completed is True

