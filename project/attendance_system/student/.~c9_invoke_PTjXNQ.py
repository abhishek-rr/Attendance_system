from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from django.http import HttpResponse
from User.models import User
from User.form import GenericCreationForm
from django.forms.models import inlineformset_factory
from .models import studentprofile
from subject.models import subject
from attendance_system.err import err
from django import forms as f
from django.contrib.auth.decorators import login_required
import student.forms as forms 
from django.db.models import Q
from attendance.models import attendance
from .functions import *
import statistics
import plotly.offline as py
import plotly.graph_objs as go
# Create your views here.
@login_required
def edit_Sprofile(request,pk):
    if request.user.is_student:
        if request.user.pk==pk:
            student=User.objects.get(pk=pk)
            Sprofile=studentprofile.objects.get(user=student)
            form=forms.edit_student(student.email,student.first_name,student.last_name,instance=Sprofile)
            form.fields['subject'].widget.attrs.update({'class':'checkbox'})
            form.fields['dob'].widget.attrs.update({'class':'date'})
            if request.method=='POST':
                form=forms.edit_student(request.POST["email"],request.POST["first_name"],request.POST["last_name"],request.POST,request.FILES)
                if form.is_valid():
                    fo=form.update(pk)
                    if 'image' in request.FILES:
                        fs=FileSystemStorage()
                        filename=fs.save(request.FILES["image"].name,request.FILES["image"])
                    return redirect("/"+request.session["type_profile"]+"/dashboard/profile/"+str(pk)+"/")
                else:
                    return HttpResponse("OOOOO")
            else:
                return render(request,'student/edit.html',{'form':form})

def new_studentform(request):
    user_form=GenericCreationForm()
    profileinlineformset= inlineformset_factory(User,studentprofile,fields=('image','mobile_number','parents_number','department','semester','dob','address','roll_no','batch','Class','subject'),widgets={'subject':f.CheckboxSelectMultiple(attrs={'class':'checkbox'})})             
    formset=profileinlineformset()
    
    if request.method=='POST':
        user_form=GenericCreationForm(request.POST)
        formset=profileinlineformset(request.POST)
        
        if user_form.is_valid():
            created_user=user_form.save(commit=False)
            created_user.is_student=True
            created_user.is_active=False
            formset = profileinlineformset(request.POST,request.FILES,instance=created_user)
            
            if formset.is_valid():
            
                created_user.save()
                formset.save()
            
                errors=[err(e="Please Reach to Admin and Register Your ID.",link=" "),err(e="Your Account is InActive It will be activated by admin.",link=" ")]
                return render(request,'error.html',{'errors':errors})

    return render(request,'student/signup.html',{"user_form":user_form,"formset":formset,})
 
@login_required
def dashboard_profile(request,pk):
    if request.user.pk == pk:
        student=User.objects.get(pk=pk)
        StudentProfile=studentprofile.objects.get(user=student)
        request.session["profile"]=str(StudentProfile.image)
        return render(request,'student/dashboard/profile.html',{'student':student,'StudentProfile':StudentProfile})
    else:
        return HttpResponse("404 bad url!")
        
@login_required
def dashboard_analysis(request,pk):
    if request.user.pk==pk:
        data=[]
        total_percent=[]
        student=User.objects.get(pk=pk)
        StudentProfile=studentprofile.objects.get(user=student)
        for sub in StudentProfile.subject.all():
            q=(Q(subject=sub)&Q(student=StudentProfile.user_id))
            att_count=attendance.objects.filter(q).count()
            att_total=totalatt(sub,StudentProfile.Class)
            percent=att_count/(att_total+0.00001)*100
            total_percent.append(percent)
            l=[sub,att_count,att_total,percent]
            data.append(l)
        labels=[water]
        
        labels=['water','air','earth','fire']
        values=[4000,2000,6000,8000]
        colors=['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']
        
        trace = go.Pie(labels=labels,values=values,hoverinfo='label + percent',textinfo='value', textfont=dict(size=20),marker=dict(colors=colors,line=dict(color='#000000',width=2)))
        graph=py.iplot([trace],filename='styled_pir_chart')        
        return render(request,'student/dashboard/analysis.html',{'student':student,'StudentProfile':StudentProfile,'data':data,'all_subjects_total':all_subjects_total,'graph':graph})
        
        
    else:
        return HttpResponse("Bad Url!!!")
        