from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class MessagePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            username='admin',
            password='password123',
            is_staff=True,
        )

    def test_anonymous_can_create_message(self):
        response = self.client.post(
            '/api/messages/',
            {
                'name': 'Visitor',
                'email': 'visitor@example.com',
                'subject': 'Hello',
                'content': 'Nice site.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_list_messages(self):
        response = self.client.get('/api/messages/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_list_messages(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get('/api/messages/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Create your tests here.
