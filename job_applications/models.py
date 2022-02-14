from django.db import models

from .utils import upload_to_file, generate_random_string
from .validators import validate_file


class CompanyManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Company.DoesNotExist:
            return None


class Company(models.Model):

    objects = CompanyManager()

    label = models.CharField(max_length=60, default="default", unique=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Company Label: {self.label} / Description: {self.description}>"


class JobManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Job.DoesNotExist:
            return None


class Job(models.Model):

    objects = JobManager()

    label = models.CharField(max_length=60, default="default")
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey('job_applications.Company', on_delete=models.SET_NULL, null=True, blank=True)
    hiring_contact = models.CharField(max_length=60, default="default")
    hiring_contact_email = models.EmailField(max_length=254)
    is_open = models.BooleanField(default=True)
    metadata = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Job Label: {self.label} / Company: {self.company.label}>"


class ApplicationManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Application.DoesNotExist:
            return None


class Application(models.Model):

    objects = ApplicationManager()

    PENDING = 1
    REVIEWING = 2
    SHORTLISTED = 3
    INTERVIEWING = 4
    ADVANCED_INTERVIEWING = 5
    REJECTED = 6
    OFFERED = 7
    HIRED = 8

    NEXT_STAGE = {
        PENDING: [REVIEWING, SHORTLISTED],
        REVIEWING: [REJECTED],
        SHORTLISTED: [INTERVIEWING],
        INTERVIEWING: [ADVANCED_INTERVIEWING, REJECTED, OFFERED],
        ADVANCED_INTERVIEWING: [REJECTED, OFFERED],
        OFFERED: [HIRED, REJECTED],
        REJECTED: [],
        HIRED: []
    }

    STAGE_TO_TASKS = {
        PENDING: {
            "description": "Checked with hiring manager whether he/she has reviewed the application?",
            "deadline": 7
        },
        REVIEWING: {
            "description": "Have you waited a few days yet?",
            "deadline": 7
        },
        SHORTLISTED: {
            "description": "Have you checked with candidate whether he has gone for the interview?",
            "deadline": 7
        },
        INTERVIEWING: {
            "description": "Have you checked with candidate on the status of his interview?",
            "deadline": 7
        },
        ADVANCED_INTERVIEWING: {
            "description": "Have you checked with candidate on the status of his advanced interview?",
            "deadline": 7
        },
        OFFERED: {
            "description": "Have you checked with candidate whether he has taken up the offer?",
            "deadline": 7
        }

    }

    categories = [
        (PENDING, "Pending"),
        (REVIEWING, "Reviewing"),
        (SHORTLISTED, "Shortlisted"),
        (INTERVIEWING, "Interviewing"),
        (ADVANCED_INTERVIEWING, "Advanced Interviewing"),
        (REJECTED, "Rejected"),
        (OFFERED, "Offered"),
        (HIRED, "Hired"),
    ]

    user = models.ForeignKey('custom_user.User', on_delete=models.CASCADE, null=False, blank=False, related_name='user')
    recruiter = models.ForeignKey('custom_user.User', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='recruiter')
    email = models.EmailField(max_length=254)
    job = models.ForeignKey('job_applications.Job', on_delete=models.CASCADE, null=False, blank=False)
    stage = models.IntegerField(
        choices=categories,
    )
    resume = models.FileField(
        upload_to=upload_to_file,
        validators=[validate_file],
        help_text="Please upload only PDF or docx files",
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Application Username: {self.user.username} / JobId: {self.job.pk} / Stage: {self.stage}>"

    @property
    def possible_next_stages(self) -> list:
        """
        retrieves the possible next stages to for the application to move into
        """

        return Application.NEXT_STAGE[self.stage]




