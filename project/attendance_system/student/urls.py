from django.urls import path,re_path
from .views import *
urlpatterns = [
    path('signup/',new_studentform,name='newstudentform'),
    path('dashboard/profile/<int:pk>/',dashboard_profile,name='dashboard_profile'),
    path('dashboard/analysis/<int:pk>/',dashboard_analysis,name='dashboard_analysis'),
    path('edit/<int:pk>/',edit_Sprofile,name='edit_form')
]
