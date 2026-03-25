from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        JOB_SEEKER = 'job_seeker', 'Job Seeker'
        RECRUITER = 'recruiter', 'Recruiter'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOB_SEEKER)

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'


class JobSeekerProfile(TimeStampedModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='job_seeker_profile')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    skills = models.ManyToManyField('jobs.Skill', blank=True, related_name='job_seekers')

    def __str__(self):
        return f'Profile for {self.user.username}'

    @property
    def profile_completion(self):
        checks = [
            bool(self.phone),
            bool(self.location),
            bool(self.bio),
            self.years_of_experience is not None,
            bool(self.resume),
            self.skills.exists(),
        ]
        return int((sum(checks) / len(checks)) * 100)


class RecruiterProfile(TimeStampedModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='recruiter_profile')
    designation = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Recruiter profile for {self.user.username}'

    @property
    def profile_completion(self):
        checks = [
            bool(self.designation),
            bool(self.phone),
            bool(self.contact_email),
            bool(self.department),
        ]
        return int((sum(checks) / len(checks)) * 100)
