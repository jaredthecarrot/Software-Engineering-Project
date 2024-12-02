from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('profile/<int:user_id>/', views.profile, name='profile')
]
