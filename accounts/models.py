from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone=models.CharField(max_length=11, blank=True, null=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username