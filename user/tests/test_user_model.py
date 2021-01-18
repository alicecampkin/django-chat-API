from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    """
    Things to test:
    - create_user method
    - create_super_user method
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='janedoe@test.com',
            full_name='Jane Doe',
            password='password123'
        )
        cls.superuser = get_user_model().objects.create_superuser(
            email='lizsmith@test.com',
            full_name='Liz Smith',
            password='password123'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'janedoe@test.com')
        self.assertEqual(self.user.full_name, 'Jane Doe')

    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, 'lizsmith@test.com')
        self.assertEqual(self.superuser.full_name, 'Liz Smith')
        self.assertTrue(self.superuser.is_admin)
        self.assertTrue(self.superuser.is_staff)

    def test_str(self):
        self.assertEqual(str(self.user), 'Jane Doe | janedoe@test.com')
