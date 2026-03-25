from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from apps.accounts.mixins import RecruiterRequiredMixin

from .forms import CompanyForm
from .models import Company


class CompanyDetailView(RecruiterRequiredMixin, DetailView):
    template_name = 'companies/company_detail.html'

    def get_object(self, queryset=None):
        return self.request.user.company


class CompanyUpdateView(RecruiterRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('company_detail')

    def get_object(self, queryset=None):
        company, _ = Company.objects.get_or_create(
            owner=self.request.user,
            defaults={
                'name': f'{self.request.user.get_full_name() or self.request.user.username} Company',
                'description': 'Tell candidates about your company.',
                'location': 'Add company location',
            },
        )
        return company

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner = self.request.user
        company.save()
        messages.success(self.request, 'Company profile saved successfully.')
        return redirect(self.success_url)
