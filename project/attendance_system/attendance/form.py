from django import forms
from django.db import models
from .models import attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model=attendance
        fields=('date_time','status','teacher','student','entry_time','subject')