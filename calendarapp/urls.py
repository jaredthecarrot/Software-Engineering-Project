from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.user_calendar, name='user_calendar'),  # Main calendar page
    path('create_event/', views.create_event, name='create_event')  # Create new event
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)