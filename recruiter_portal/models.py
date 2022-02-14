from django.db import models

from job_applications.models import Application
from job_applications.utils import time_now_utc, create_deadline

from typing import Optional


class TaskManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Task.DoesNotExist:
            return None


class Task(models.Model):

    objects = TaskManager()

    REVIEWING_DEAD_LINE: int = 7
    REVIEWING_DESCRIPTION: str = "Checked with hiring manager whether he/she has reviewed the application?"

    recruiter = models.ForeignKey('custom_user.User', on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey('job_applications.Application', on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey('job_applications.Job', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        recruiter_name = None
        if self.recruiter:
            recruiter_name = self.recruiter.username

        return f"<Task Recruiter: {recruiter_name} / Application: {self.application} / Job: {self.job}>"

    @staticmethod
    def proceed_to_next_task(application: Application) -> Optional["Task"]:
        """
        Create a new task based the current stage of application as reference. No new tasks will be created if
        application reaches either rejected or hired stage.
        """

        # no further tasks will be generated once an application reaches rejected or hired status
        if application.stage in [Application.REJECTED, Application.HIRED]:
            return None

        time_now = time_now_utc()
        due_date = create_deadline(time=time_now, days=Application.STAGE_TO_TASKS[application.stage]["deadline"])
        task: Task = Task.objects.create(job=application.job, application=application, recruiter=application.recruiter,
                                         description=Application.STAGE_TO_TASKS[application.stage]["description"],
                                         due_date=due_date)

        return task
