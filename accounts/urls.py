from django.urls import path

from .views import *

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("verify-email/", verify_email, name="verify_email"),
    path("resend-otp/", resend_otp, name="resend_otp"),
]
