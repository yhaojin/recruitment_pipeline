from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from typing import Optional, Tuple


class CustomUserManager(UserManager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except User.DoesNotExist:
            return None


class User(AbstractUser):

    objects = CustomUserManager()

    JOB_SEEKER = 1
    RECRUITER = 2

    categories = [
        (JOB_SEEKER, "Job Seeker"),
        (RECRUITER, "Recruiter"),
    ]

    category = models.IntegerField(
        choices=categories, default=JOB_SEEKER
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<User Username: {self.username} / Email: {self.email}>"


class NotificationManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Notification.DoesNotExist:
            return None


class Notification(models.Model):

    objects = NotificationManager()

    user = models.ForeignKey('custom_user.User', on_delete=models.CASCADE, null=False, blank=False)
    viewed = models.BooleanField(default=False)
    job = models.ForeignKey('job_applications.Job', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Notification Username: {self.user.username} / Viewed: {self.viewed} / Description: {self.description}>"
