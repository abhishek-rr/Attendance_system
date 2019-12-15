from django.urls import path,re_path
from .views import *

urlpatterns=[path('temporarysave/',save),
             path('apply/',Apply),]

