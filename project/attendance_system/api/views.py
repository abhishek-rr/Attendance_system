from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from User.models import User
import attendance_system.views as v
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render,HttpResponse
from attendance_system.err import err
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect,redirect,reverse
from django import forms as form
import teacher.form as forms 
from User.models import User
from attendance_system.err import err
from User.form import GenericCreationForm
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from teacher.models import teacherprofile
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from classes.models import classes
from datetime import datetime
from django.template.loader import get_template
from django.template import Template
from teacher.graph_def import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
import statistics
from student.functions import *


# Create your views here.
def Login(request):
    if request.method == "POST":
          print(request.body)
    if request.method == "POST" : 
        user=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            login(request,user)
        
            if request.user.is_teacher:
                request.session["type_profile"]="teacher"
                return redirect('/api/teacher/dashboard/profile/'+str(request.user.pk)+'/')
            elif request.user.is_student:
                request.session["type_profile"]="student"
                return redirect('/api/student/dashboard/profile/'+str(request.user.pk)+'/')
            else:
                request.session["type_profile"]=""
                return HttpResponse(json.dumps([{'ERROR':'Admin and Staff Not Allowed Here!!!'},]))
        else:
            return HttpResponse(json.dumps([{'ERROR':'Invalid Credentials!! Check Once.'},]))
  
        
    else:
        print(request.META)
        print("__________________________________________")
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        if request.session.is_empty():
            print("Hello")
            return render(request,'apiCSRFTWT.html',{})
        elif request.session['type_profile']=='teacher':
            user = authenticate(request)
            return redirect('/api/teacher/dashboard/profile/'+str(request.user.pk)+'/')
        elif request.session['type_profile']=='student':
            user = authenticate(request)
            print('-------------------')
            print(request.user)
            return redirect('/api/student/dashboard/profile/'+str(request.user.pk)+'/')
        else:
            logout(request) #This is Because You may have logged in as Admin or Staff(neither Teacher nor Student)
            return HttpResponse(json.dumps([{'ERROR':'You May be Logged In as Staff or Admin(Not Allowed)'},]))

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse(json.dumps([{'success':"Sucessfully Logged OUT"},]))
    else:
        return HttpResponse(json.dumps([{'ERROR':'Error LoggingOut!!!'},]))
    
    
@login_required()
def teacher_dashboard_profile(request,pk):
    print(request.user)
    print(request.user.is_authenticated)
    if request.user.pk == pk:
        teacher=User.objects.get(pk=pk)
        TeacherProfile=teacherprofile.objects.get(user=teacher)
        request.session["profile"]=str(TeacherProfile.image)
        print(teacher)
        print(TeacherProfile)
        return HttpResponse(serializers.serialize('json',[teacher,TeacherProfile]))
    else:
        return HttpResponse(json.dumps([{'ERROR':'Profile Not Found!!'},]))

        
@login_required
def student_dashboard_profile(request,pk):
    if request.user.pk == pk:
        student=User.objects.get(pk=pk)
        StudentProfile=studentprofile.objects.get(user=student)
        request.session["profile"]=str(StudentProfile.image)
        data = serializers.serialize('json',[student,StudentProfile])
        d = json.loads(data)
        print(d)
        return HttpResponse(json.dumps(d))
    else:
        return HttpResponse(json.dumps({'ERROR':'Profile Not Found!!'}))


@login_required
def student_dashboard_analysis(request,pk):
    if request.user.pk==pk:
        data=[]
        total_percent=[]
        student=User.objects.get(pk=pk)
        StudentProfile=studentprofile.objects.get(user=student)
        for sub in StudentProfile.subject.all():
            q=(Q(subject=sub)&Q(student=StudentProfile.user_id)&Q(Class=StudentProfile.Class))
            att_count=attendance.objects.filter(q).count()
            time_list=[]
            att_list=attendance.objects.filter(q).values_list('date_time',flat=True)
            for time in att_list:
                time=time-timedelta(seconds=time.second,minutes=time.minute)
                if time not in time_list:
                    time_list.append(time)
            len(time_list)
            att_total=totalatt(sub,StudentProfile.Class)
            percent=round(att_count/(att_total+0.00001)*100)
            total_percent.append(percent)
            l=[sub,att_count,att_total,percent]
            data.append(l)
        all_subjects_total=statistics.mean(total_percent)
        graph=piechart(StudentProfile)
        graph2=bar_graph(data)
        jsonProfile=serializers.serialize('json',[student,StudentProfile])
        dictPython = json.loads(jsonProfile)
        jsonData=json.dumps({'data':data,'all_subjects_total':all_subjects_total,'graph':[graph,graph2]})
        dictPython[2]=json.loads(jsonData)
        return HttpResponse(json.dumps(dictPython))

    else:
        return HttpResponse(json.dumps({'ERROR':'Profile Not Found!!'}))

