from django import forms
from .models import Profile
from PIL import Image


class PhotoForm(forms.ModelForm):
    """
    A form for uploading profile pictures. This is used with Cropper.js on the front-end.
    x, y, width & height are supplied by Cropper.js and are used here to crop the photo
    using Pillow.
    """

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('profile_picture', 'x', 'y', 'width',
                  'height')

    def save(self, user, commit=True):

        profile = super().save()

        profile.user = user

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.profile_picture)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.profile_picture.path)

        profile.save()

        return profile


class ProfileForm(forms.ModelForm):
    """
    A form to create/update a user profile. Includes all fields apart from
    profile_picture, which is handled in PhotoForm.
    """

    class Meta:
        model = Profile
        fields = ('bio', 'display_name',)
