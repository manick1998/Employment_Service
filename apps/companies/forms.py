from django import forms

from apps.accounts.forms import BootstrapFormMixin

from .models import Company


class CompanyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'description', 'website', 'logo', 'location', 'is_active')
