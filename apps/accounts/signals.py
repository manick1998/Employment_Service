from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import JobSeekerProfile, RecruiterProfile, User


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.role == User.Role.JOB_SEEKER:
        JobSeekerProfile.objects.get_or_create(user=instance)
    elif instance.role == User.Role.RECRUITER:
        RecruiterProfile.objects.get_or_create(user=instance)
