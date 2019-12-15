"""attendance_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path,include
import attendance_system.views as views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.homepageview),
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('user/',include('User.urls')),
    path('student/',include('student.urls')),
    path('att/',include('temp_att.urls')),
    path('attendance/',include('attendance.urls')),
    path(r'api/',include('api.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
