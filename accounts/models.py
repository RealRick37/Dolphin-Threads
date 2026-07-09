from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone=models.CharField(max_length=11, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class EmailOTP(models.Model):
    email=models.EmailField(unique=True)
    code=models.CharField(max_length=6)
    attempts=models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300