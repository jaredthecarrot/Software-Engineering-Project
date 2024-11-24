from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
