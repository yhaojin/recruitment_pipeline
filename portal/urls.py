from django.urls import path
from .views import JobsIndexView


urlpatterns = [
    path('', JobsIndexView.as_view(), name='jobs_portal'),
]
