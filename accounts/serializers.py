from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, validators=[validate_password])
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=CustomUser
        fields=[
            "username",
            "email",
            "password",
            "password2",
        ]
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value
    
    def validate(self, attrs):
        if attrs["password"]!=attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(username=validated_data["username"], email=validated_data["email"],
            password=validated_data["password"])
    
class ProfileSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source="user.username", read_only=True)
    email=serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model=Profile
        fields=[
            "username",
            "email",
            "phone",
            "address",
            "created_at",
        ]