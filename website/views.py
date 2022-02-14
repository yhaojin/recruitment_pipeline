from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class LandingPageView(TemplateView):
    """
    TemplateView of the main landing page of the website.
    """

    template_name = 'website/landing_page.html'
