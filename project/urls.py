"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403, handler500
from django.urls import include, path

handler404 = 'courses.views.view_404'
handler500 = 'courses.views.view_500'
handler403 = 'courses.views.view_403'

app_name = 'project'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('grades/', views.grades, name='grades'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.index, name='index'),
    path('', include('users.urls',namespace='users')),
    path('', include('courses.urls',namespace='courses')),
    path('', include('blog.urls',namespace='blogs')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)