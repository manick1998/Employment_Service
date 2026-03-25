from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.applications.models import JobApplication
from apps.companies.models import Company
from apps.jobs.models import Job, Skill


class Command(BaseCommand):
    help = 'Seed the database with demo users, company, jobs, skills, and applications.'

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user, created = User.objects.get_or_create(
            username='adminuser',
            defaults={
                'email': 'admin@example.com',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin_user.set_password('AdminPass123!')
            admin_user.save()

        recruiter, created = User.objects.get_or_create(
            username='recruiter1',
            defaults={
                'email': 'recruiter@example.com',
                'role': User.Role.RECRUITER,
                'first_name': 'Riya',
                'last_name': 'Recruiter',
            },
        )
        if created:
            recruiter.set_password('RecruiterPass123!')
            recruiter.save()

        seeker, created = User.objects.get_or_create(
            username='seeker1',
            defaults={
                'email': 'seeker@example.com',
                'role': User.Role.JOB_SEEKER,
                'first_name': 'Arjun',
                'last_name': 'Seeker',
            },
        )
        if created:
            seeker.set_password('SeekerPass123!')
            seeker.save()

        skill_names = ['Python', 'Django', 'REST API', 'SQL', 'Bootstrap']
        skills = [Skill.objects.get_or_create(name=name)[0] for name in skill_names]

        company, _ = Company.objects.get_or_create(
            owner=recruiter,
            defaults={
                'name': 'Manicks Recruitment Services',
                'description': 'A demo company for local testing.',
                'website': 'https://example.com',
                'location': 'Bengaluru',
                'is_active': True,
            },
        )

        job_one, _ = Job.objects.get_or_create(
            recruiter=recruiter,
            company=company,
            title='Junior Django Developer',
            defaults={
                'description': 'Build server-rendered Django applications and internal APIs.',
                'location': 'Remote',
                'salary_min': 400000,
                'salary_max': 700000,
                'employment_type': Job.EmploymentType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.ENTRY,
                'status': Job.Status.PUBLISHED,
                'is_active': True,
            },
        )
        job_one.skills.set(skills[:4])

        job_two, _ = Job.objects.get_or_create(
            recruiter=recruiter,
            company=company,
            title='Frontend Support Engineer',
            defaults={
                'description': 'Work with templates, Bootstrap, and light JavaScript enhancements.',
                'location': 'Hyderabad',
                'salary_min': 350000,
                'salary_max': 600000,
                'employment_type': Job.EmploymentType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.ENTRY,
                'status': Job.Status.PUBLISHED,
                'is_active': True,
            },
        )
        job_two.skills.set([skills[4], skills[0]])

        JobApplication.objects.get_or_create(
            job=job_one,
            job_seeker=seeker,
            defaults={
                'status': JobApplication.Status.APPLIED,
                'cover_letter': 'I am excited to learn and contribute.',
            },
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write('Admin: adminuser / AdminPass123!')
        self.stdout.write('Recruiter: recruiter1 / RecruiterPass123!')
        self.stdout.write('Job seeker: seeker1 / SeekerPass123!')
