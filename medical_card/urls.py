"""medical_card URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import *
from registration.views import signup, enter_email_confirm_code, successful_registration
from django.conf.urls.i18n import i18n_patterns

urlpatterns = []

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('welcome.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/signup', LogoutView.as_view(), name='logout'),
    path('accounts/registration/', signup, name='signup'),
    path('accounts/reset/done', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('accounts/reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html'),
        name='password_reset'),
    path('accounts/password_change/', PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'),
        name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('accounts/enter-email-confirm-code/', enter_email_confirm_code, name='email-confirm-page'),
    path('accounts/registration/successful/', successful_registration, name='successful_registration'),
)
