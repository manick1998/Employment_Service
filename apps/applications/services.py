from django.db import IntegrityError, transaction

from .models import JobApplication


def submit_application(*, job_seeker, job, cover_letter=''):
    resume_name = ''
    if hasattr(job_seeker, 'job_seeker_profile') and job_seeker.job_seeker_profile.resume:
        resume_name = job_seeker.job_seeker_profile.resume.name

    try:
        with transaction.atomic():
            application = JobApplication.objects.create(
                job=job,
                job_seeker=job_seeker,
                cover_letter=cover_letter,
                resume_snapshot_name=resume_name,
            )
    except IntegrityError as exc:
        raise ValueError('You have already applied for this job.') from exc
    return application
