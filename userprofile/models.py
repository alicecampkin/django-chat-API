from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


def get_filename(self, filename):
    """ Generates a custom filename for uploads based on author's username and the post's creation date """

    extension = filename.split('.')[-1]
    t = datetime.now()
    datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

    return f"uploads/profiles/{self.user.username}_{datetime_str}.{extension}"


class Profile(models.Model):
    user = models.OneToOneField(
        USER_MODEL, null=True, on_delete=models.CASCADE)

    display_name = models.CharField(max_length=255, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        blank=True, null=True, upload_to=get_filename)

    def __str__(self):
        return f"{self.user.email}"
