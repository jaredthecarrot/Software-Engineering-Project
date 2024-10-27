from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from uuid import UUID

urlpatterns = [
    path('chat_view', views.chat_view, name='chat_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)