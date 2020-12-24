from django.test import TestCase
from user.forms import ProfileForm

PROFILE_FIELDS = ['bio', 'profile_picture']

class TestProfileForm(TestCase):

    def test_fields(self):
        """ Tests all desired fields are present on the form. """

        form = ProfileForm()

        for field in PROFILE_FIELDS:
            self.assertIn(field, form.fields)