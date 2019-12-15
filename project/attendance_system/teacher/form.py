from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import teacherprofile
from django.db import models
from subject.models import subject
from User.models import User
from django.core.files.storage import FileSystemStorage

attr=('image','class_TG','start_student_rollno','last_student_rollno','mobile_number','department','dob','address','years_of_experience','last_lecture','subject','education','is_HOD',)


class TeacherProfileDataForm(forms.ModelForm):
    
    class Meta:
        model = teacherprofile
        fields =attr
        
class TeacherProfileDataChangeForm(forms.ModelForm):
    
    class Meta:
        model = teacherprofile
        fields = attr+('teacher_id',)
        
class edit(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    subject=forms.ModelMultipleChoiceField( queryset=subject.objects.all(),widget=forms.CheckboxSelectMultiple())
    class Meta:
        model=teacherprofile
        fields=('email','first_name','last_name','subject')+attr
        
    def __init__(self,em,fn,ln,*args,**kwargs):
        super(edit,self).__init__(*args,**kwargs)
        self.initial["email"]=em
        self.initial["first_name"]=fn
        self.initial["last_name"]=ln
        
        
    def update(self,pk,commit=True):
        if commit:
            uu=User.objects.filter(pk=pk).update(email=self.cleaned_data["email"],
                                    first_name=self.cleaned_data["first_name"],
                                    last_name=self.cleaned_data["last_name"])
            tu=teacherprofile.objects.filter(user=User.objects.get(pk=pk)).update(
                                                                            mobile_number=self.cleaned_data["mobile_number"],
                                                                            department=self.cleaned_data["department"],
                                                                            dob=self.cleaned_data["dob"],
                                                                            address=self.cleaned_data["address"],
                                                                            years_of_experience=self.cleaned_data["years_of_experience"],
                                                                            last_lecture=self.cleaned_data["last_lecture"],
                                                                            education=self.cleaned_data["education"],
                                                                            class_TG=self.cleaned_data['class_TG'])
            if self.cleaned_data['image']:
                teacherprofile.objects.filter(user=User.objects.get(pk=pk)).update(image=self.cleaned_data["image"])  #handled differently from other update soo that leaving the field empty should not clear image
                        
            su=False                                                    
            teacherprofile.objects.get(user=User.objects.get(pk=pk)).subject.clear()
            for sub in self.cleaned_data["subject"]:
                su=teacherprofile.objects.get(user=User.objects.get(pk=pk)).subject.add(sub)
                                            
            return (uu and tu)
            
            
        
    