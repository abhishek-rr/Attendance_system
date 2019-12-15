from django.contrib import admin
from django.urls import path,include
from .views import Login,display,Logout

urlpatterns = [
    path('',Login),
    path('display/',display),
    path('logout/',Logout),
]
