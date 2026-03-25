from django.test import TestCase
from django.urls import reverse


class ApiSmokeTests(TestCase):
    def test_api_jobs_endpoint_loads(self):
        response = self.client.get(reverse('api-jobs-list'))
        self.assertEqual(response.status_code, 200)
