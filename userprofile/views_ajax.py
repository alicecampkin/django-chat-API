from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from .models import Profile
from .forms import PhotoForm
import json

USER_MODEL = get_user_model()


@require_POST
@login_required
def change_profile_picture(request):

    user = request.user

    profile = get_object_or_404(Profile, user=user)
    form = PhotoForm(request.POST, request.FILES, instance=profile)

    if form.is_valid():

        profile = form.save(user, commit=False)
        response = {
            'status': 'SUCCESS',
            'photo_url': profile.profile_picture.url
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        raise ValidationError('Form Invalid')
