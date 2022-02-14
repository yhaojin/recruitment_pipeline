from django.urls import path
from .views import CustomLogInView

urlpatterns = [
    path('login/', CustomLogInView.as_view(), name="account_login"),
]
