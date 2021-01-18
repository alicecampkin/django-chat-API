from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(
        template_name='user/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('password/change', auth_views.PasswordChangeView.as_view(
        template_name='user/password_change_form.html'), name='password_change'),
    path('password/change/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='user/password_change_done.html'), name='password_change_done'),
    path('password/reset', auth_views.PasswordResetView.as_view(
        template_name='user/password_reset_form.html'), name='password_reset'),
    path('password/reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'), name='password_reset_complete')
]
