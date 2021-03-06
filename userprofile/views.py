from .forms import ProfileForm
from .models import Profile
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

USER_MODEL = get_user_model()


@login_required
def edit_profile(request):
    """ A view to edit a user profile """

    user = request.user

    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=user)
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            success_url = reverse('author', args=[user.username])

            return HttpResponseRedirect(success_url)

    else:
        profile = Profile.objects.get(user=user)
        form = ProfileForm(instance=profile)

    context = {
        'page-title': user.username,
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)
