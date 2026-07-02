from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.password_validation import validate_password

User=get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام کاربری"}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمز عبور"}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "تکرار رمز عبور"}))

    def clean_username(self):
        username=self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری وجود داره، ی چیز دیگه امتحان کن !")
        return username
    
    def clean_email(self):
        email=self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلا ثبت شده *-*")
        return email
    
    def clean(self):
        cleaned_data=super().clean()

        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        if password!=confirm_password:
            raise forms.ValidationError("رمز های عبوری وارد شده بکسان نیستن!!!")
        return cleaned_data
    


    def clean_password(self):
        password=self.cleaned_data["password"]

        validate_password(password)

        return password


    def save(self):
        user=User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "phone",
            "address",
        ]

        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }