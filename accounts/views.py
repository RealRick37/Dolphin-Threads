from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import random
from django.core.mail import send_mail
from .forms import VerifyOTPForm
from django.contrib.auth import get_user_model
from .models import EmailOTP
from django.utils import timezone
# Create your views here.

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if form.is_valid():

            request.session["register_data"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
            }

            otp = str(random.randint(100000, 999999))

            EmailOTP.objects.update_or_create(email=form.cleaned_data["email"], defaults={"code": otp})

            send_mail(subject="Email Verification", message=f"Your verification code is: {otp}", from_email=None,
                    recipient_list=[form.cleaned_data["email"]],)

            messages.success(request, "کد تایید به ایمیل شما ارسال شد.")

            return redirect("verify_email")

    return render(request, "register.html", {"form": form})


def verify_email(request):
    form = VerifyOTPForm(request.POST or None)

    data = request.session.get("register_data")

    if not data:
        messages.error(request, "ابتدا ثبت نام را انجام بده.")
        return redirect("register")

    otp_obj = EmailOTP.objects.filter(
        email=data["email"]).first()

    if not otp_obj:
        messages.error(request, "کد تاییدی پیدا نشد.")
        return redirect("register")

    passed = (timezone.now() - otp_obj.created_at).total_seconds()
    remaining = max(0, int(300 - passed))

    if request.method == "POST":

        if otp_obj.attempts >= 5:
            messages.error(request, "تعداد تلاش مجاز تمام شده است.")
            return redirect("register")

        if otp_obj.is_expired():
            messages.error(request, "زمان کد تایید به پایان رسیده است.")
            return redirect("verify_email")

        if form.is_valid():

            user_otp = form.cleaned_data["otp"]

            if user_otp == otp_obj.code:

                User.objects.create_user(username=data["username"], email=data["email"], password=data["password"])

                otp_obj.delete()

                request.session.pop("register_data", None)

                messages.success(request, "حساب کاربری با موفقیت ساخته شد.")

                return redirect("login")

            otp_obj.attempts += 1
            otp_obj.save()

            messages.error(request, f"کد اشتباه است. ({otp_obj.attempts}/5)")

    return render(request, "emails/verify_email.html", {"form": form, "remaining": remaining,})

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


def login_view(request):
    form=AuthenticationForm(request, data=request.POST or None)
    
    if request.user.is_authenticated:
        return redirect("home")

    if request.method=="POST":
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            messages.success(request, f"خوش اومدی {user.username}")
            return redirect("product_list")
    return render(request, "login.html", {"form":form})

def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدی.")
    return redirect("login")


# ---- profile -----

@login_required
def profile_view(request):
    profile=request.user.profile
    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile=request.user.profile
    form=ProfileForm(request.POST or None, instance=profile)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل بروزرسانی شد.")

            return redirect("profile")
    return render(request, "edit_profile.html", {"form": form})

