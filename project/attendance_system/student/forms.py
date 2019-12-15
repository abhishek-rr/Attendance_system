from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import ModelForm
from .models import studentprofile,User
from subject.models import subject

attributes=('student_id','image','mobile_number','parents_number','department','semester','dob','address','roll_no','batch','Class')

class StudentProfileDataForm(forms.ModelForm):
    class Meta:
        model=studentprofile
        fields=('student_id','image','mobile_number','parents_number','department','semester','dob','address','roll_no','batch','Class')
        
class StudentProfileDataFormAdmin(forms.ModelForm):
    class Meta:
        model=studentprofile
        fields=('student_id','RFID')
        
class edit_student(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    subject=forms.ModelMultipleChoiceField(queryset=subject.objects.all(),widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model= studentprofile
        fields=attributes + ('email','first_name','last_name','subject')
        
    def __init__(self,em,fn,ln,*args,**kwargs):
        super(edit_student,self).__init__(*args,**kwargs)
        self.initial["email"]=em
        self.initial["first_name"]=fn
        self.initial["last_name"]=ln
        
    def update(self,pk,commit=True):
        if commit:
            uu=User.objects.filter(pk=pk).update(email=self.cleaned_data["email"],
                                    first_name=self.cleaned_data["first_name"],
                                    last_name=self.cleaned_data["last_name"])
            su=studentprofile.objects.filter(user=User.objects.get(pk=pk)).update(
                                                                            mobile_number=self.cleaned_data["mobile_number"],
                                                                            parents_number=self.cleaned_data["parents_number"],
                                                                            department=self.cleaned_data["department"],
                                                                            dob=self.cleaned_data["dob"],
                                                                            address=self.cleaned_data["address"],
                                                                            semester=self.cleaned_data["semester"],
                                                                            roll_no=self.cleaned_data["roll_no"],
                                                                            batch=self.cleaned_data["batch"],
                                                                            Class=self.cleaned_data['Class'])
            if self.cleaned_data['image']:
                studentprofile.objects.filter(user=User.objects.get(pk=pk)).update(image=self.cleaned_data["image"])  #handled differently from other update soo that leaving the field empty should not clear image
                        
            flag=False                                                    
            studentprofile.objects.get(user=User.objects.get(pk=pk)).subject.clear()
            for sub in self.cleaned_data["subject"]:
                flag=studentprofile.objects.get(user=User.objects.get(pk=pk)).subject.add(sub)
                                            
            return (uu and su)