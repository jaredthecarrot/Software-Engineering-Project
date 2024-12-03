from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.avif')
    location = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    
    def __str__(self):
        return self.user.username
    

# New OrganizationProfile model
class OrganizationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to existing User
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)  # Link to existing Profile
    organization_name = models.CharField(max_length=100)
    organization_description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.organization_name
