from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default = 'blank_profile_picture.avif')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username
    
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    posts_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Stats"
