from django import forms
from django.db import models
from .models import subject

class subjectCreationForm(forms.ModelForm):
    
    class Meta:
        model=subject
        fields=['name','code','semester']
    
class editSubjectForm(forms.ModelForm):
    
    class Meta:
        model=subject
        fields=['name','code','semester']
        

        