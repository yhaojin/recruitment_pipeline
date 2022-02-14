from django.urls import path
from .views import RecruiterIndexView, take_on_application_view, SaveTaskChangesView


urlpatterns = [
    path('', RecruiterIndexView.as_view(), name='recruiter_portal'),
    path('take_on_application/<application_pk>/', take_on_application_view, name='take_on_application'),
    path('save_task_changes/<task_pk>/', SaveTaskChangesView.as_view(), name='save_task_changes'),
]
