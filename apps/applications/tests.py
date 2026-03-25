from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.companies.models import Company
from apps.jobs.models import Job

from .models import JobApplication


class ApplicationTests(TestCase):
    def setUp(self):
        self.recruiter = get_user_model().objects.create_user(username='recruiter', email='r@example.com', password='StrongPass123!', role='recruiter')
        self.seeker = get_user_model().objects.create_user(username='seeker', email='s@example.com', password='StrongPass123!', role='job_seeker')
        self.other_recruiter = get_user_model().objects.create_user(username='other', email='o@example.com', password='StrongPass123!', role='recruiter')
        self.company = Company.objects.create(owner=self.recruiter, name='Hiring Co', description='Demo', location='Delhi')
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            company=self.company,
            title='QA Engineer',
            description='Test apps',
            location='Remote',
            status=Job.Status.PUBLISHED,
        )

    def test_job_seeker_can_apply_once(self):
        self.client.force_login(self.seeker)
        response = self.client.post(reverse('job_apply', kwargs={'slug': self.job.slug}), {'cover_letter': 'Ready to help'})
        self.assertRedirects(response, reverse('applied_jobs'))
        second_response = self.client.post(reverse('job_apply', kwargs={'slug': self.job.slug}), {'cover_letter': 'Trying again'})
        self.assertRedirects(second_response, reverse('applied_jobs'))
        self.assertEqual(JobApplication.objects.filter(job=self.job, job_seeker=self.seeker).count(), 1)

    def test_only_owner_recruiter_can_view_applicants(self):
        JobApplication.objects.create(job=self.job, job_seeker=self.seeker)
        self.client.force_login(self.other_recruiter)
        response = self.client.get(reverse('job_applicants', kwargs={'slug': self.job.slug}))
        self.assertEqual(response.status_code, 403)
