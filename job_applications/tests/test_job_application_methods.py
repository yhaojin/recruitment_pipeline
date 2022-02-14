from django.test import TestCase, SimpleTestCase
from django.core.files import File
from custom_user.models import User
from job_applications.utils import time_now_utc
from job_applications.models import Company, Application, Job

from django.utils import timezone as tz

import math
import re
import os
from django.conf import settings


def validate_email(email: str) -> bool:

    # regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return True if (re.fullmatch(regex, email)) else False


class JobsTestObject:

    def __init__(self):

        time_now = time_now_utc()
        self.time_now = time_now

        self.user1 = User.objects.create(
            username="user1",
            email="user1@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )

        self.user2 = User.objects.create(
            username="user2",
            email="user2@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user3 = User.objects.create(
            username="user3",
            email="user3@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user4 = User.objects.create(
            username="user4",
            email="user4@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user5 = User.objects.create(
            username="user5",
            email="user5@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user6 = User.objects.create(
            username="user6",
            email="user6@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user7 = User.objects.create(
            username="user7",
            email="user7@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )
        self.user8 = User.objects.create(
            username="user8",
            email="user8@example.com",
            category=User.JOB_SEEKER,
            password='pass@123',
        )

        self.recruiter = User.objects.create(
            username="recruiter1",
            email="recruter1@example.com",
            category=User.RECRUITER,
            password='pass@123',
        )

        self.recruiter2 = User.objects.create(
            username="recruiter2",
            email="recruter2@example.com",
            category=User.RECRUITER,
            password='pass@123',
        )

        self.company_google = Company.objects.create(
            label='Google',
            description="Google LLC is an American multinational technology company that specializes in "
                        "Internet-related services and products",
            metadata='Tech;Internet',
        )
        self.company_singtel = Company.objects.create(
            label='Singtel',
            description="Singapore Telecommunications Limited, commonly known as Singtel and stylised as SingTel,"
                        "is a Singaporean telecommunications conglomerate and one of the four major telcos operating "
                        "in the country.",
            metadata='Telco;Utilities',
        )
        self.company_dbs = Company.objects.create(
            label='DBS Bank',
            description="DBS Bank Limited (abbreviation: DBS) is a Singaporean multinational banking and financial "
                        "services corporation headquartered at the Marina Bay Financial Centre in the Marina Bay "
                        "district of Singapore. ",
            metadata='Bank;Finance',
        )
        self.job_google_full_stack = Job.objects.create(
            label="Full stack engineer",
            description="You will work as a Full stack engineer.",
            company=self.company_google,
            hiring_contact="James Roger",
            hiring_contact_email="james_roger@google.com",
            is_open=True,
            metadata="Full stack;Engineer;Tech",
        )
        self.job_google_back_end = Job.objects.create(
            label="Back End engineer",
            description="You will work as a Back End engineer.",
            company=self.company_google,
            hiring_contact="James Roger",
            hiring_contact_email="james_roger@google.com",
            is_open=True,
            metadata="Back End;Engineer;Tech",
        )
        self.job_singtel_data_analyst = Job.objects.create(
            label="Data Analyst",
            description="You will work as a data analyst.",
            company=self.company_singtel,
            hiring_contact="James Tan",
            hiring_contact_email="james_tan@singtel.com",
            is_open=True,
            metadata="Data Analyst;Data;Tech",
        )
        self.job_dbs_product_manager = Job.objects.create(
            label="Product Manager",
            description="You will work as a product manager.",
            company=self.company_dbs,
            hiring_contact="Olivia Tan",
            hiring_contact_email="olivia_tan@dbs.com",
            is_open=True,
            metadata="Product Manager;Tech",
        )

        with open(os.path.join(os.path.join(settings.BASE_DIR, 'job_applications', 'tests'), 'empty_resume.pdf'), 'rb') as local_file:
            self.empty_resume = File(local_file)

            self.application_pending = Application.objects.create(
                user=self.user1, recruiter=self.recruiter, email=self.user1.email,
                job=self.job_google_full_stack, stage=Application.PENDING, resume=self.empty_resume,
            )
            self.application_reviewing = Application.objects.create(
                user=self.user2, recruiter=self.recruiter, email=self.user2.email,
                job=self.job_dbs_product_manager, stage=Application.REVIEWING, resume=self.empty_resume,
            )
            self.application_shortlisted = Application.objects.create(
                user=self.user3, recruiter=self.recruiter, email=self.user3.email,
                job=self.job_dbs_product_manager, stage=Application.SHORTLISTED, resume=self.empty_resume,
            )
            self.application_interviewing = Application.objects.create(
                user=self.user4, recruiter=self.recruiter, email=self.user4.email,
                job=self.job_dbs_product_manager, stage=Application.INTERVIEWING, resume=self.empty_resume,
            )
            self.application_advanced_interviewing = Application.objects.create(
                user=self.user5, recruiter=self.recruiter2, email=self.user5.email,
                job=self.job_dbs_product_manager, stage=Application.ADVANCED_INTERVIEWING, resume=self.empty_resume,
            )
            self.application_rejected = Application.objects.create(
                user=self.user6, recruiter=self.recruiter2, email=self.user6.email,
                job=self.job_dbs_product_manager, stage=Application.REJECTED, resume=self.empty_resume,
            )
            self.application_offered = Application.objects.create(
                user=self.user7, recruiter=self.recruiter2, email=self.user7.email,
                job=self.job_dbs_product_manager, stage=Application.OFFERED, resume=self.empty_resume,
            )
            self.application_hired = Application.objects.create(
                user=self.user8, recruiter=self.recruiter2, email=self.user8.email,
                job=self.job_dbs_product_manager, stage=Application.HIRED, resume=self.empty_resume,
            )

            # create tasks for each one of the applications



class JobApplicationMethodsTestCase(TestCase):

    def setUp(self):

        self.jobs_test_object = JobsTestObject()

    def test_possible_next_stages(self):
        """
        Test case which tests that possible_next_stage will correctly provide the possible next stages according to the
        business logic.
        """

        assert len(self.jobs_test_object.application_pending.possible_next_stages) == len([Application.REVIEWING,
                                                                                           Application.SHORTLISTED])
        for next_stage in self.jobs_test_object.application_pending.possible_next_stages:
            assert next_stage in [Application.REVIEWING, Application.SHORTLISTED]

        assert len(self.jobs_test_object.application_reviewing.possible_next_stages) == len([Application.REJECTED])
        for next_stage in self.jobs_test_object.application_reviewing.possible_next_stages:
            assert next_stage in [Application.REJECTED]

        assert len(self.jobs_test_object.application_shortlisted.possible_next_stages) == len([Application.INTERVIEWING])
        for next_stage in self.jobs_test_object.application_shortlisted.possible_next_stages:
            assert next_stage in [Application.INTERVIEWING]

        assert len(self.jobs_test_object.application_interviewing.possible_next_stages) == len([Application.ADVANCED_INTERVIEWING,
                                                                                                Application.OFFERED,
                                                                                                Application.REJECTED])
        for next_stage in self.jobs_test_object.application_interviewing.possible_next_stages:
            assert next_stage in [Application.ADVANCED_INTERVIEWING, Application.OFFERED, Application.REJECTED]

        assert len(self.jobs_test_object.application_advanced_interviewing.possible_next_stages) == len([Application.OFFERED,
                                                                                                         Application.REJECTED])
        for next_stage in self.jobs_test_object.application_advanced_interviewing.possible_next_stages:
            assert next_stage in [Application.OFFERED, Application.REJECTED]

        assert len(self.jobs_test_object.application_offered.possible_next_stages) == len([Application.HIRED, Application.REJECTED])
        for next_stage in self.jobs_test_object.application_offered.possible_next_stages:
            assert next_stage in [Application.HIRED, Application.REJECTED]




