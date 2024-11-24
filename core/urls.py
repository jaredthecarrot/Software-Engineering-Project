from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('about', views.about, name='about')
    
    #path('logout', views.logout, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('about', views.about, name='about'),
    path('select-account-type/', views.select_account_type, name='select_account_type'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
