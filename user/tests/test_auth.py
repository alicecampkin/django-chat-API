from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_MODEL = get_user_model()


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestAuth(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def test_obtain_token(self):
        login_url = reverse('token_obtain_pair')

        payload = {
            'email': 'jane.deux@test.com',
            'full_name': 'Jane Deux',
            'password': 'pawwsord1234'
        }

        create_user(**payload)

        response = self.client.post(
            login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_bad_password_no_token(self):
        login_url = reverse('token_obtain_pair')

        payload = {
            'email': 'jane.deux@test.com',
            'full_name': 'Jane Deux',
            'password': 'wrongpawwsord1234'
        }

        create_user(**payload)

        response = self.client.post(
            login_url, {'email': 'jane.deux@test.com', 'password': 'password'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('refresh', response.data)
        self.assertNotIn('access', response.data)
