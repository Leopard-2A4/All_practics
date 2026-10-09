from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars_image_directory_path", blank=True)

def avatars_image_directory_path(instance: Profile, filename: str):
    pk = instance.user.pk
    return f"avatars/user_{pk}images/{filename}"