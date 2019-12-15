from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import User


class GenericCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields =('username','email','first_name','last_name')
        
class Admin_GenericCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','email','is_active','first_name','last_name')
        

class GenericChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields  = ('username','email','is_active','first_name','last_name')
        #exclude = ('password1','password2','username','is_student','is_teacher')
        
class Admin_GenericChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        #exclude = ('password1','password2','username','is_student','is_teacher')
        fields = ('username','email','is_active','first_name','last_name','is_student','is_teacher')
        