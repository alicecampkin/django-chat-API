from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    We need to extend the default UserCreationForm to accommodate the extra fields.
    This form is displayed when we create a user in admin from another model.
    We can also reuse the form in the UI for registration.
    """
    class Meta:
        model = User
        fields = ("email", "full_name")


class UserChangeForm(forms.ModelForm):
    """
    This is the form that's displayed when you edit the user. This won't affect how user information is displayed
    in admin. Instead, it controls the pop-up form when user objects are editted from another model.
    This form needs to be updated to show fields that aren't present in the AbstractBaseUser.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'is_active', 'is_admin')
