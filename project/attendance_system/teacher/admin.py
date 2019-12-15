from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .form import TeacherProfileDataForm,TeacherProfileDataChangeForm
from .models import teacherprofile

# Register your models here.
class TeacherUserAdmin(admin.ModelAdmin):
    add_form = None
    form = TeacherProfileDataChangeForm
    model = teacherprofile
    list_display = ['user']
    fieldsets=(
            ('Profile',{'fields':('teacher_id','is_HOD','RFID')}),
        )
        
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(teacherprofile,TeacherUserAdmin)