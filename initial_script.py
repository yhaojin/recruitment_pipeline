import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment_pipeline.settings")
django.setup()

from django.conf import settings
from django.core.files import File

"""
This script creates the initial accounts, companies and jobs
"""

from job_applications.models import Company, Job
from custom_user.models import User
from django.contrib.auth.hashers import make_password

companies = [
    ("Google",
     "Google LLC is an American multinational technology company that specializes in "
     "Internet-related services and products",
     "Tech;Internet"),
    ("Singtel",
     "Singapore Telecommunications Limited, commonly known as Singtel and stylised as SingTel, "
     "is a Singaporean telecommunications conglomerate and one of the four major telcos operating in the country.",
     "Telco;Utilities"),
    ("DBS Bank",
     "DBS Bank Limited (abbreviation: DBS) is a Singaporean multinational banking and financial services "
     "corporation headquartered at the Marina Bay Financial Centre in the Marina Bay district of Singapore. ",
     "Bank;Finance"),
]

for label, description, metadata in companies:

    company: Company = Company.objects.get_or_none(label=label)
    if not company:
        Company.objects.create(
            label=label,
            description=description,
            metadata=metadata,
        )
    else:
        company.label = label
        company.description = description
        company.metadata = metadata
        company.save()


jobs = [
    ("Full stack engineer",
     "You will work as a Full stack engineer.",
     "Google",
     "James Roger",
     "james_roger@google.com",
     "Full stack;Engineer;Tech"),
    ("Back End engineer",
     "You will work as a Back End engineer.",
     "Google",
     "James Roger",
     "james_roger@google.com",
     "Back End;Engineer;Tech"),
    ("Data Analyst",
     "You will work as a data analyst.",
     "Singtel",
     "James Tan",
     "james_tan@singtel.com",
     "Data Analyst;Data;Tech"),
    ("Product Manager",
     "You will work as a product manager.",
     "DBS Bank",
     "Olivia Tan",
     "olivia_tan@dbs.com",
     "Product Manager;Tech"),
]

for label, description, company_name, hiring_contact, hiring_contact_email, metadata in jobs:

    company: Company = Company.objects.get(label=company_name)
    job: Job = Job.objects.get_or_none(label=label, company=company)
    if not job:
        Job.objects.create(
            label=label,
            description=description,
            company=company,
            hiring_contact=hiring_contact,
            hiring_contact_email=hiring_contact_email,
            metadata=metadata,
        )
    else:
        job.label = label
        job.description = description
        job.company = company
        job.hiring_contact = hiring_contact
        job.hiring_contact_email = hiring_contact_email
        job.metadata = metadata
        job.save()


users = [
    ("user1", "David", "Tan", "user1@example.com", User.JOB_SEEKER, "password12345"),
    ("user2", "Richard", "Soh", "user2@example.com", User.JOB_SEEKER, "password12345"),
    ("recruiter1", "Samuel", "Lim", "recruiter1@example.com", User.RECRUITER, "password12345"),
    ("recruiter2", "Aaron", "Tan", "recruiter2@example.com", User.RECRUITER, "password12345"),
]

for username, first_name, last_name, email, category, password in users:

    user: User = User.objects.get_or_none(username=username)
    if not user:
        User.objects.create(
            category=category,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=False,
            is_active=True,
            password=make_password(password),
        )
    else:
        user.category = category
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_staff = False
        user.is_active = True
        user.password = make_password(password)
        user.save()