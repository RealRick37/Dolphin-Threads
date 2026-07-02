from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "حساب کاربری با موفقیت ساخته شد."
            )

            return redirect("login")

    return render(
        request,
        "register.html",
        {"form": form}
    )

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

