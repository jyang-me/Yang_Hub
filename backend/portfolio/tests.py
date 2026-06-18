from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ProjectPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            username='admin',
            password='password123',
            is_staff=True,
        )

    def test_anonymous_can_list_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_project(self):
        response = self.client.post(
            '/api/projects/',
            {'title': 'Portfolio', 'summary': 'A project'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_create_project(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            '/api/projects/',
            {'title': 'Portfolio', 'summary': 'A project'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Create your tests here.
