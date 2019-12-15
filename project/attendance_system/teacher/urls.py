from django.urls import path,re_path
from .views import *

urlpatterns=[
        path('signup/',new_teacherform,name='newform'),
        #path('login/',Login,name='login'),
        #path('logout/',Logout,name='logout'),
        path('dashboard/profile/<int:pk>/',dashboard_profile,name='dashboard_profile'),
        path('dashboard/analysis/<int:pk>/',dashboard_analysis,name='dashboard_analysis'),
        path('edit/<int:pk>/',edit_Tprofile,name='editprofile'),
        path('dashboard/sheets',sheets),
        path('its/ajax/',firstAJAX),
        path('first/',first),
        ]