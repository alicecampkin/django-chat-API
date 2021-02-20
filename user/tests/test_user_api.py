from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_MODEL = get_user_model()


class TestAPICreateUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.create_user_url = reverse("register")

    def tearDown(self):
        users = USER_MODEL.objects.all()
        for user in users:
            user.delete()

    def test_register_user(self):
        """ Tests we can create a user with a valid payload """

        payload = {
            "email": "janedoe@test.com",
            "full_name": "janedoe",
            "password": "password123"
        }

        response = self.client.post(self.create_user_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = USER_MODEL.objects.get(**response.data)

        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_email_uniqueness(self):
        """ Tests that a registration request is rejected if the email is not unique."""

        user1 = USER_MODEL.objects.create(
            email="tom@test.com",
            full_name="Tom Test",
            password="password123"
        )

        payload = {
            "email": "tom@test.com",
            "full_name": "Tommo Test",
            "password": "password123"
        }

        response = self.client.post(self.create_user_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_registration_fields(self):

        payloads = [
            {
                "email": "",
                "full_name": "Tommo Test",
                "password": "password123"
            },
            {
                "email": "tom2@test.com",
                "full_name": "",
                "password": "password123"
            },
            {
                "email": "tom3@test.com",
                "full_name": "Tom Test",
                "password": ""
            },
        ]

        for payload in payloads:
            response = self.client.post(self.create_user_url, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response = None


class TestAPIAuthenticate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create(
            email="t@test.com",
            full_name='Tom Test',
            password='password1234'
        )

        cls.client = APIClient()
        cls.login_url = reverse("login")

    def test_authenticate(self):
        """ test a valid email and password authenticates the user. """

        payload = {
            "email": "t@test.com",
            "password": "password1234"
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
