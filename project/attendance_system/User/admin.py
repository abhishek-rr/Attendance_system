from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .form import Admin_GenericChangeForm,Admin_GenericCreationForm
from .models import User

# Register your models here.
class GenericUserAdmin(UserAdmin):
    add_form = Admin_GenericCreationForm
    form = Admin_GenericChangeForm
    model = User
    list_display = ['username','email']
    fieldsets=(
            (None,{'fields':('username','email','password')}),
            ('PERSONAL INFO',{'fields':('first_name','last_name')}),
            ('Privelege',{'fields':('is_active','is_staff','is_superuser',)})
        )
    
admin.site.unregister(Group)
admin.site.register(User,GenericUserAdmin)