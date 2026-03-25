from django.urls import path

from .views import ApplyToJobView, ApplicationStatusUpdateView, AppliedJobListView, RecruiterApplicantListView

urlpatterns = [
    path('apply/<slug:slug>/', ApplyToJobView.as_view(), name='job_apply'),
    path('mine/', AppliedJobListView.as_view(), name='applied_jobs'),
    path('job/<slug:slug>/applicants/', RecruiterApplicantListView.as_view(), name='job_applicants'),
    path('<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='application_status_update'),
]
