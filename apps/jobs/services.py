from .models import Job


def close_job(job):
    job.status = Job.Status.CLOSED
    job.is_active = False
    job.save(update_fields=['status', 'is_active', 'updated_at'])
    return job
