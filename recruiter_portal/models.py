from django.db import models

# Create your models here.

class TaskManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Task.DoesNotExist:
            return None


class Task(models.Model):

    objects = TaskManager()

    recruiter = models.ForeignKey('custom_user.User', on_delete=models.CASCADE, null=False, blank=False)
    job = models.ForeignKey('job_applications.Job', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Notification Username: {self.user.username} / Viewed: {self.viewed} / Description: {self.description}>"