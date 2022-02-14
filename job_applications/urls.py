from django.urls import path
from .views import JobApplicationView, download_resume_view, JobView, change_application_stage

urlpatterns = [
    path('<job_pk>/', JobView.as_view(), name='job'),
    path('apply/<application_pk>/', JobApplicationView.as_view(), name='job_application'),
    path('download_resume/<application_pk>/', download_resume_view, name='download_resume'),
    path('change_application_stage/<application_pk>/', change_application_stage, name='change_application_stage'),
]
