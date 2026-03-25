from django.urls import path

from .views import (
    PublicJobDetailView,
    PublicJobListView,
    RecruiterJobCloseView,
    RecruiterJobCreateView,
    RecruiterJobListView,
    RecruiterJobUpdateView,
)

urlpatterns = [
    path('', PublicJobListView.as_view(), name='job_list'),
    path('recruiter/', RecruiterJobListView.as_view(), name='recruiter_job_list'),
    path('recruiter/new/', RecruiterJobCreateView.as_view(), name='job_create'),
    path('recruiter/<slug:slug>/edit/', RecruiterJobUpdateView.as_view(), name='job_edit'),
    path('recruiter/<slug:slug>/close/', RecruiterJobCloseView.as_view(), name='job_close'),
    path('<slug:slug>/', PublicJobDetailView.as_view(), name='job_detail'),
]
