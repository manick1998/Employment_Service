from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Company


class CompanyModelTests(TestCase):
    def test_recruiter_can_own_company(self):
        user = get_user_model().objects.create_user(username='recruiter', email='r@example.com', password='StrongPass123!', role='recruiter')
        company = Company.objects.create(owner=user, name='Demo Co', description='Demo', location='Pune')
        self.assertEqual(company.owner, user)
        self.assertTrue(company.slug)
