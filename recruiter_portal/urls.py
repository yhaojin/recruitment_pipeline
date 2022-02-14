from django.urls import path
from .views import RecruiterIndexView


urlpatterns = [
    path('', RecruiterIndexView.as_view(), name='recruiter_portal'),
]
