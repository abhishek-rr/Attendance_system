from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import ModelForm
from .models import studentprofile

attributes=('student_id','image','mobile_number','parents_number','department','semester','dob','address','roll_no','batch','Class')

class StudentProfileDataForm(forms.ModelForm):
    class Meta:
        model=studentprofile
        fields=('student_id','image','mobile_number','parents_number','department','semester','dob','address','roll_no','batch','Class')
        
class edit_student(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms
    subject=forms.ModelMultipleChoiceField(queryset=subject.objects.all,widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model= studentprofile
        fields=attributes + ('email','first_name','last_name')
        
    def __init__(self,em,fn,ln,*args,**kwargs):
        super()