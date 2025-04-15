from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .views import register, login_view, logout_user, profile, edit_profile_view, confirm_email

app_name = 'accounts'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_user, name="logout_user"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile_view, name="edit_profile"),
    path("password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("accounts:password_change_done"),
            template_name="password_change.html",
        ),
        name="password_change",
    ),
    path("password_change_done",
        PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("confirm_email/", confirm_email, name="confirm_email"),
    ]