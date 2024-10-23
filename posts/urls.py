from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from uuid import UUID

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('add-post-comment/<uuid:post_id>/', views.add_comment, name='add-post-comment'),  # Change to <uuid:post_id>
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)