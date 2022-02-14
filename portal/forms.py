from django.forms import ModelForm
from job_applications.models import Application


class _ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = ("resume", "email", "job")


class ApplicationForm(_ApplicationForm):

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')

        super(_ApplicationForm, self).__init__(*args, **kwargs)

        self.fields['resume'].help_text = f"Please upload only docx or pdf files."
        self.fields['email'].initial = self.user.email


