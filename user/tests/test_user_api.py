from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_MODEL = get_user_model()


class TestUserAPI(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.create_user_url = reverse('register')

    def test_register_user(self):
        """ Tests we can create a user with a valid payload """

        payload = {
            'email': 'janedoe@test.com',
            'full_name': 'janedoe',
            'password': 'password123'
        }

        response = self.client.post(self.create_user_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = USER_MODEL.objects.get(**response.data)

        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', response.data)
