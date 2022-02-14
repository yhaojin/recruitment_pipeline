from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


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