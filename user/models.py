from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):

    def create_user(self, email, password, full_name):
        """ Creates and saves a user """

        self.validate_required_fields(email, full_name, display_name, username)

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            display_name=display_name,
            username=username.lower()
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, full_name):
        """ Creates and saves a superuser """

        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            display_name=display_name,
            username=username
        )

        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)
        return user

    def validate_required_fields(self, email, full_name):
        """ Raises value errors if any required field is None """

        if not email:
            raise ValueError('Please provide a valid email')
        elif not username:
            raise ValueError('Please provide a valid username')
        elif not full_name:
            raise ValueError('Please provide a name')

        return


class User(AbstractBaseUser):
    """ Custom user model users email as the identifier"""

    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100)

    account_created = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.full_name} | {self.email}'

    # has_perm and has_module_perms required to view users in Admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
