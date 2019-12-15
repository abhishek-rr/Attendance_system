from django.urls import path,re_path
from .views import *

urlpatterns=[
        path('login/',Login),
        path('logout/',Logout),
    ]