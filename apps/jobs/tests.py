from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.companies.models import Company

from .models import Job, Skill


class JobTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='recruiter', email='r@example.com', password='StrongPass123!', role='recruiter')
        self.company = Company.objects.create(owner=self.user, name='Tech Co', description='Demo company', location='Chennai')
        self.skill = Skill.objects.create(name='Django')

    def test_job_slug_is_created(self):
        job = Job.objects.create(
            recruiter=self.user,
            company=self.company,
            title='Backend Developer',
            description='Build APIs',
            location='Remote',
            status=Job.Status.PUBLISHED,
        )
        job.skills.add(self.skill)
        self.assertTrue(job.slug)

    def test_job_list_page_loads(self):
        Job.objects.create(
            recruiter=self.user,
            company=self.company,
            title='Backend Developer',
            description='Build APIs',
            location='Remote',
            status=Job.Status.PUBLISHED,
        )
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Backend Developer')

    def test_recruiter_can_create_job_from_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('job_create'),
            {
                'title': 'Platform Engineer',
                'description': 'Build scalable Django features',
                'location': 'Bengaluru',
                'salary_min': 500000,
                'salary_max': 900000,
                'employment_type': Job.EmploymentType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.MID,
                'status': Job.Status.PUBLISHED,
                'is_active': 'on',
                'skills': [self.skill.pk],
            },
        )

        self.assertRedirects(response, reverse('recruiter_job_list'))
        created_job = Job.objects.get(title='Platform Engineer')
        self.assertEqual(created_job.recruiter, self.user)
        self.assertEqual(created_job.company, self.company)
        self.assertEqual(created_job.skills.count(), 1)

    def test_job_create_form_defaults_to_published(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].fields['status'].initial, Job.Status.PUBLISHED)

    def test_public_search_returns_new_published_job(self):
        Job.objects.create(
            recruiter=self.user,
            company=self.company,
            title='AI Engineer',
            description='Work on AI products',
            location='Chennai',
            status=Job.Status.PUBLISHED,
        )

        response = self.client.get(reverse('job_list'), {'title': 'AI Engineer'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Engineer')

    def test_recruiter_search_returns_own_job(self):
        Job.objects.create(
            recruiter=self.user,
            company=self.company,
            title='AI Engineer',
            description='Work on AI products',
            location='Chennai',
            status=Job.Status.DRAFT,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('recruiter_job_list'), {'title': 'AI Engineer'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Engineer')
