from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import User


class GenericCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields =('username','email','first_name','last_name')
        
class Admin_GenericCreationForm(UserCreationForm):
    i
    class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','email','is_active','first_name','last_name','is_student','is_teacher')
        

class GenericChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('username','email','is_active','first_name','last_name')
        
class Admin_GenericChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('username','email','is_active','first_name','last_name','is_student','is_teacher')
        