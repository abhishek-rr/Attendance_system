from django.urls import path,re_path
from .views import *

urlpatterns=[path('fetch/',fetch),
             path('update/',update),]