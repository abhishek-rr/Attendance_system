from django.urls import path,re_path
from .views import *

urlpatterns=[
        path('user/login/',Login),
        path('user/logout/',Logout),
        path('teacher/dashboard/profile/<int:pk>/',teacher_dashboard_profile,name='teacher_dashboard_profile'),
        path('student/dashboard/profile/<int:pk>/',student_dashboard_profile,name='student_dashboard_profile'),
    ]
