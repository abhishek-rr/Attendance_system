from django.contrib import admin
from .models import studentprofile
from .forms import StudentProfileDataFormAdmin

class StudentUserAdmin(admin.ModelAdmin):
    form=StudentProfileDataFormAdmin
    add_form=None
    
admin.site.register(studentprofile, StudentUserAdmin)
