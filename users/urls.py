from operator import index
from django.contrib import admin
from django.urls import path
from users.views import about, contact, grades
from . views import HomeView, login_user, Profile, logout_user, sign_up, teacher_request, edit_profile
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

app_name = 'users'

urlpatterns = [
    path('about/', about, name='about'),
    path('index/', index, name='index'),
    path('grades/', grades, name='grades'),
    path('contact/', contact, name='contact'),
    path('register', views.register, name="register"),
    path('login', login_user, name="login"),
    path('profile/', views.Profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('logout_user', logout_user, name="logout_user"),
    path('sign_up', sign_up, name="sign_up"),
    path('teacher_request/', teacher_request, name='teacher_request'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)