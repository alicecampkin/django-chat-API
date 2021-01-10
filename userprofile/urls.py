from django.urls import path
from . import views
from . import views_ajax as ajax_views

urlpatterns = [
    path('edit', views.edit_profile, name='edit_profile'),
    path('edit/profilephoto', ajax_views.change_profile_picture, name='change_profile_picture'),
]
