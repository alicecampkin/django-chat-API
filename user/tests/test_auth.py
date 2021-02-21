from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_MODEL = get_user_model()

class TestAuth(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create(
            email='jane.deux@test.com',
            password='pawwsord1234'
        )

    def test_obtain_token(self):
        login_url = reverse('token_obtain_pair')

        payload = {
            'email': self.user.email,
            'password': self.user.password
        }

        response = APIClient.post(login_url, payload)

        self.assertEqual(response.status_code, 200)
