from django.contrib import admin
from .models import attendance
from .form import AttendanceForm

# Register your models here.
admin.site.register(attendance)
