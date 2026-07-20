from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("resend-otp/", resend_otp, name="resend_otp"),
]
