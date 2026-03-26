from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import TimeStampedModel


class JobApplication(TimeStampedModel):
    class Status(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        REVIEWING = 'reviewing', 'Reviewing'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        REJECTED = 'rejected', 'Rejected'

    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    cover_letter = models.TextField(blank=True)
    resume_snapshot_name = models.CharField(max_length=255, blank=True)
    recruiter_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=('job', 'job_seeker'), name='unique_application_per_job_seeker'),
        ]

    def __str__(self):
        return f'{self.job_seeker.username} -> {self.job.title}'

    def clean(self):
        if self.job_seeker_id and self.job_seeker.role != self.job_seeker.Role.JOB_SEEKER:
            raise ValidationError('Only job seekers can apply for jobs.')
