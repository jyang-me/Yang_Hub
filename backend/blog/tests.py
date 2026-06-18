from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class BlogPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            username='admin',
            password='password123',
            is_staff=True,
        )
        self.user = get_user_model().objects.create_user(
            username='user',
            password='password123',
        )

    def test_anonymous_can_list_posts(self):
        response = self.client.get('/api/posts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_post(self):
        response = self.client.post(
            '/api/posts/',
            {'title': 'Test post', 'content': '# Hello'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/posts/',
            {'title': 'Test post', 'content': '# Hello'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_post(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            '/api/posts/',
            {'title': 'Test post', 'content': '# Hello'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Create your tests here.
