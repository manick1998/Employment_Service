from django import forms

from apps.accounts.forms import BootstrapFormMixin

from .models import JobApplication


class JobApplicationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('cover_letter',)


class ApplicationStatusUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('status', 'recruiter_notes')
