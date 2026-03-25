from .models import JobApplication


def applied_jobs_for_user(user):
    return JobApplication.objects.filter(job_seeker=user).select_related('job', 'job__company')


def applicants_for_job(job, recruiter):
    if job.recruiter_id != recruiter.id:
        return JobApplication.objects.none()
    return JobApplication.objects.filter(job=job).select_related('job_seeker', 'job')
