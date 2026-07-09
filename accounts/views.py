from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from .forms import VerifyOTPForm
from django.contrib.auth import get_user_model
from .models import EmailOTP, Profile
from django.utils import timezone
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

User = get_user_model()

class RegisterView(FormView):
    template_name="register.html"
    form_class=RegisterForm
    success_url=reverse_lazy("verify_email")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["register_data"]={
            "username": form.cleaned_data["username"],
            "email": form.cleaned_data["email"],
            "password": form.cleaned_data["password"],
        }

        otp=str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(email=form.cleaned_data["email"], defaults={"code": otp})

        send_mail(subject="Email Verification", message=f"Your verification code is: {otp}", from_email=None, recipient_list=[form.cleaned_data["email"]],)

        messages.success(self.request, "کد تائید به ایمیل شما ارسال شد.")

        return super().form_valid(form)

class VerifyEmailView(FormView):
    template_name = "emails/verify_email.html"
    form_class = VerifyOTPForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):

        self.register_data = request.session.get("register_data")

        if not self.register_data:
            messages.error(request, "ابتدا ثبت نام را انجام بده.")
            return redirect("register")

        self.otp_obj = EmailOTP.objects.filter(email=self.register_data["email"]).first()

        if not self.otp_obj:
            messages.error(request, "کد تاییدی پیدا نشد.")
            return redirect("register")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        passed = (timezone.now() - self.otp_obj.created_at).total_seconds()

        context["remaining"] = max(0, int(300 - passed))

        return context

    def form_valid(self, form):

        if self.otp_obj.attempts >= 5:

            messages.error(self.request, "تعداد تلاش مجاز تمام شده است.")

            return redirect("register")

        if self.otp_obj.is_expired():

            messages.error(self.request, "زمان کد تایید به پایان رسیده است.")

            return redirect("verify_email")

        user_otp = form.cleaned_data["otp"]

        if user_otp == self.otp_obj.code:

            User.objects.create_user(username=self.register_data["username"], email=self.register_data["email"],
                password=self.register_data["password"],)

            self.otp_obj.delete()
            self.request.session.pop("register_data", None)

            messages.success(self.request, "حساب کاربری با موفقیت ساخته شد.")

            return super().form_valid(form)

        self.otp_obj.attempts += 1
        self.otp_obj.save()

        messages.error(self.request, f"کد اشتباه است. ({self.otp_obj.attempts}/5)")

        return self.form_invalid(form)


def resend_otp(request):

    data = request.session.get("register_data")

    if not data:
        return redirect("register")

    otp_obj = EmailOTP.objects.filter(email=data["email"]).first()

    if otp_obj:

        seconds = (timezone.now() - otp_obj.created_at).total_seconds()

        if seconds < 60:

            messages.error(request, f"لطفا {int(60-seconds)} ثانیه دیگر صبر کن.")

            return redirect("verify_email")

    otp = str(random.randint(100000, 999999))

    EmailOTP.objects.update_or_create(email=data["email"], defaults={"code": otp, "attempts": 0,})

    send_mail(
        subject="Email Verification",
        message=f"Your verification code is: {otp}",
        from_email=None,
        recipient_list=[data["email"]],
    )

    messages.success(request, "کد جدید ارسال شد.")

    return redirect("verify_email")


class UserLoginView(LoginView):
    template_name="login.html"
    authentication_form=AuthenticationForm
    redirect_authenticated_user=True

    def form_valid(self, form):
        response=super().form_valid(form)
        messages.success(self.request, f"خوش اومدی {self.request.user.username}")
        return response
    
    def get_success_url(self):
        return reverse_lazy("home")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "با موفقیت خارج شدی.")
        return super().dispatch(request, *args, **kwargs)


# ---- profile -----
class ProfileView(LoginRequiredMixin, DetailView):
    model=Profile
    template_name="profile.html"
    context_object_name="profile"

    def get_object(self):
        return self.request.user.profile


class EditProfileView(LoginRequiredMixin, UpdateView):
    model=Profile
    form_class=ProfileForm
    template_name="edit_profile.html"

    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy("profile")
    
    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, "پروفایل بروزرسانی شد.")

        return response

