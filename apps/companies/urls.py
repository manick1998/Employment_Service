from django.urls import path

from .views import CompanyDetailView, CompanyUpdateView

urlpatterns = [
    path('my-company/', CompanyDetailView.as_view(), name='company_detail'),
    path('my-company/edit/', CompanyUpdateView.as_view(), name='company_edit'),
]
