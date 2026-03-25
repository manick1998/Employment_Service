from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountFlowTests(TestCase):
    def test_job_seeker_signup_creates_profile(self):
        response = self.client.post(reverse('job_seeker_signup'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testseeker',
            'email': 'testseeker@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('job_seeker_dashboard'))
        user = get_user_model().objects.get(username='testseeker')
        self.assertEqual(user.role, user.Role.JOB_SEEKER)
        self.assertTrue(hasattr(user, 'job_seeker_profile'))

    def test_recruiter_dashboard_requires_recruiter_role(self):
        user = get_user_model().objects.create_user(username='seeker', email='s@example.com', password='StrongPass123!', role='job_seeker')
        self.client.force_login(user)
        response = self.client.get(reverse('recruiter_dashboard'))
        self.assertEqual(response.status_code, 403)
