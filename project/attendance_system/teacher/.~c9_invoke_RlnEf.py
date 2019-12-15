from django.shortcuts import render,HttpResponseRedirect,redirect,reverse
from django import forms as form
import teacher.form as forms 
from User.models import User
from attendance_system.err import err
from User.form import GenericCreationForm
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import teacherprofile
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from classes.models import classes
from datetime import datetime
from django.template.loader import get_template
from django.template import Template
from .graph_def import *
from django.views.decorators.csrf import csrf_exempt


app_name='teacher'

# Create your views here.
#
@login_required()
def edit_Tprofile(request,pk):
    if request.user.is_teacher:
        if request.user.pk == pk:
            teacher = User.objects.get(pk=pk)
            Tprofile = teacherprofile.objects.get(user = teacher)
            form = forms.edit(teacher.email,teacher.first_name,teacher.last_name,instance=Tprofile)
            form.fields['last_lecture'].widget.attrs.update({'class':'datetime'})
            form.fields['subject'].widget.attrs.update({'class':'checkbox'})
            form.fields['dob'].widget.attrs.update({'class':'date'})
            
            if request.method == 'POST':
                form=forms.edit(request.POST["email"],request.POST["first_name"],request.POST["last_name"],request.POST,request.FILES)
                if form.is_valid():
                    fo=form.update(pk)
                    if 'image' in request.FILES:
                        fs=FileSystemStorage()
                        filename=fs.save(request.FILES["image"].name,request.FILES["image"])
                    return redirect("/"+request.session["type_profile"]+"/dashboard/profile/"+str(pk)+"/")
                else:
                    return HttpResponse("OOOOO")
            else:
                return render(request,'teacher/edit.html',{"form" : form})
              
        else:
            return HttpResponse('I')
    else:
        return HttpResponse('II')


def new_teacherform(request):
    
    user_form =GenericCreationForm()
    profileinlineformset = inlineformset_factory(User,teacherprofile,fields=('image','class_TG','start_student_rollno','last_student_rollno','mobile_number','department','address','years_of_experience','education','subject','dob','last_lecture'),
                                                widgets={'subject':form.CheckboxSelectMultiple(attrs={'class':'checkbox'})})
    formset = profileinlineformset()
    formset.forms[0].fields['last_lecture'].widget.attrs.update({'class':'datetime'})
    
    formset.forms[0].fields['dob'].widget.attrs.update({'class':'date'})
    if request.method == 'POST':
        user_form = GenericCreationForm(request.POST,request.FILES)
        formset = profileinlineformset(request.POST,request.FILES)
        
        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            created_user.is_teacher=True
            created_user.is_active=False
            formset = profileinlineformset(request.POST,request.FILES,instance=created_user)
            
            if formset.is_valid():
                #fs=FileSystemStorage()
                #filename=fs.save(request.FILES["image"].name,request.FILES["image"])
                created_user.save()
                formset.save()
                #user=authenticate(username=created_user.username,password=created_user.password)
                #if user is not None:
                #    login(request,user)
                #    return redirect('dashboard',pk=user.pk)

                errors=[err(e="Please Reach to Admin and Register Your ID.",link=" "),err(e="Your Account is InActive It will be activated by admin.",link=" ")]
                return render(request,'error.html',{'errors':errors})
    
    return render(request,'teacher/signup.html',{
            "pk":None,
            "user_form": user_form,
            "formset": formset,
        
        })

@login_required()
def dashboard_profile(request,pk):
    if request.user.pk == pk:
        teacher=User.objects.get(pk=pk)
        TeacherProfile=teacherprofile.objects.get(user=teacher)
        request.session["profile"]=str(TeacherProfile.image)
        return render(request,'teacher/dashboard/profile.html',{'teacher':teacher,'TeacherProfile':TeacherProfile})
    else:
        return HttpResponse("404 bad URL!!!!")
        

@login_required()
@csrf_exempt
def dashboard_analysis(request,pk):
    if request.user.pk == pk:
        teacher=User.objects.get(pk=pk)
        TeacherProfile=teacherprofile.objects.get(user=teacher)
        Classes = classes.objects.all()

        date = "{}".format(datetime.now())[0:10]
        if request.method == 'POST':
            if not 'search' in request.POST:
                date = request.POST['date']
                print("HURRY")
                if TeacherProfile.is_HOD:
                    Class = int(request.POST['class'][0])
            else:
                name = request.POST['search']
        elif request.method == 'GET':
            
            if TeacherProfile.is_HOD:
                Class=0
                
        if not TeacherProfile.is_HOD:
            Class=TeacherProfile.class_TG_id
            
        if TeacherProfile.is_HOD ==True:
            if not 'search' in request.POST:
                div=[draw_time_histogram(date,'day',Class,5),draw_time_histogram(date,'week',Class,5),draw_time_histogram(date,'month',Class,5)]
                display = get_template('teacher/dashboard/HOD.html')
                display=display.render({'classes':Classes,'date':date,'graph':div})
            else:
                display = get_template('teacher/dashboard/HO_search.html')
                atten=searcher(name,TeacherProfile.class_TG.pk,TeacherProfile.is_HOD)
                print(name)
                display = display.render({'classes':Classes,'class_id':TeacherProfile.class_TG_id,'date':date,'name':name,'atten':atten})
        
        else:
            if not 'search' in request.POST:
                div=[draw_time_histogram(date,'day',TeacherProfile.class_TG.pk,5),draw_time_histogram(date,'week',TeacherProfile.class_TG.pk,5),draw_time_histogram(date,'month',TeacherProfile.class_TG.pk,5)]
                display = get_template('teacher/dashboard/Teachers.html')
                Def=[defaulter(date,'day',Class,5),defaulter(date,'week',Class,5),defaulter(date,'month',Class,5)]
                display=display.render({'classes':Classes,'class_id':TeacherProfile.class_TG_id,'date':date,'graph':div,'def':Def})
            else:
                display = get_template('teacher/dashboard/Teachers_search.html')
                atten=searcher(name,TeacherProfile.class_TG.pk,TeacherProfile.is_HOD)
                print(name)
                display = display.render({'classes':Classes,'class_id':TeacherProfile.class_TG_id,'date':date,'name':name,'atten':atten})
        
        return render(request,'teacher/dashboard/analysis.html',{'teacher':teacher,'TeacherProfile':TeacherProfile,'display':display})
    else:
        return HttpResponse("404 bad URL!!!!")
        
def sheets(request):
    return render(request,'teacher/dashboard/sheets.html',{})