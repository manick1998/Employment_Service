from django.db.models import Count, Q

from .models import Job, Skill


def public_jobs_queryset(filters=None):
    filters = filters or {}
    queryset = Job.objects.published().select_related('company', 'recruiter').prefetch_related('skills')

    title = filters.get('title')
    location = filters.get('location')
    skill = filters.get('skill')
    salary_min = filters.get('salary_min')
    salary_max = filters.get('salary_max')

    if title:
        queryset = queryset.filter(Q(title__icontains=title) | Q(description__icontains=title))
    if location:
        queryset = queryset.filter(location__icontains=location)
    if skill:
        queryset = queryset.filter(skills=skill)
    if salary_min:
        queryset = queryset.filter(Q(salary_min__gte=salary_min) | Q(salary_max__gte=salary_min))
    if salary_max:
        queryset = queryset.filter(Q(salary_min__lte=salary_max) | Q(salary_max__lte=salary_max))

    return queryset.distinct().order_by('-created_at')


def recruiter_jobs_queryset(recruiter):
    return (
        Job.objects.filter(recruiter=recruiter)
        .select_related('company')
        .prefetch_related('skills')
        .annotate(applicant_count=Count('applications'))
        .order_by('-created_at')
    )


def recruiter_filtered_jobs_queryset(recruiter, filters=None):
    filters = filters or {}
    queryset = recruiter_jobs_queryset(recruiter)

    title = filters.get('title')
    location = filters.get('location')
    skill = filters.get('skill')
    status = filters.get('status')

    if title:
        queryset = queryset.filter(Q(title__icontains=title) | Q(description__icontains=title))
    if location:
        queryset = queryset.filter(location__icontains=location)
    if skill:
        queryset = queryset.filter(skills=skill)
    if status:
        queryset = queryset.filter(status=status)

    return queryset.distinct().order_by('-created_at')


def skill_choices_queryset():
    return Skill.objects.all().order_by('name')
