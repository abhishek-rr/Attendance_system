from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('login/',Login),
    path('display/',display),
    path('logout/',Logout)
]