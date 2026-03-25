from rest_framework import permissions, viewsets

from apps.applications.models import JobApplication
from apps.jobs.selectors import public_jobs_queryset

from .serializers import JobApplicationSerializer, JobSerializer


class PublicJobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['title', 'description', 'location', 'company__name', 'skills__name']
    filterset_fields = ['employment_type', 'experience_level', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']

    def get_queryset(self):
        return public_jobs_queryset(self.request.query_params)


class MyApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != user.Role.JOB_SEEKER:
            return JobApplication.objects.none()
        return JobApplication.objects.filter(job_seeker=user).select_related('job', 'job__company').prefetch_related('job__skills')
