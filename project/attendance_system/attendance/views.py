from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import attendance
from django.db.models import Q
from datetime import datetime,timedelta,date
import calendar
from classes.models import *
from django.template.loader import get_template
from student.models import *
from teacher.models import *
from STCrelation.models import *

# Create your views here.
@csrf_exempt
def fetch(request):
    print(request.POST)
    print("Hello")
    Class=request.POST['Class'][0]
    subject=request.POST['subject'][0]
    da=datetime.strptime(request.POST['date'],'%Y-%m-%d').date()
    headers=[]
    print(Class)
    print(subject)
    print(da)
    print(lecture(da,Class,subject))
    for h in lecture(da,Class,subject):
        headers.append(h)
    Class=classes.objects.get(id=Class)
    rollno=[x for x in range(int(Class.rollcall_start),int(Class.rollcall_end))]
    data=[]
    for roll in rollno:
        present=[str(roll),[]]
        for lec in headers:
            q=Q(subject=subject) & Q(Class=Class) & Q(date_time__lt=lec+timedelta(hours=1)) & Q(date_time__gte=lec)
            if studentprofile.objects.filter(roll_no=str(roll)).values_list('pk',flat=True):
                id=studentprofile.objects.filter(roll_no=str(roll)).values_list('pk',flat=True)[0]
                q=q & Q(student=id)
                if attendance.objects.filter(q):
                    present[1].append('P')
                else:
                    present[1].append('A')
            else:
                present[1].append('A')
        count=0
        for ele in present[1]:
            if ele == 'P':
                count+=1
        present.append(round(count/(len(headers)+0.00001)*100))
        data.append(present)
        
        
        
    header=[str(h.date())+" "+str(h.time()) for h in headers]
    header.append("% Attendance")
    pres=["Total Att",[],"______"]
    for i in range(0,len(data[0][1])):
        co=0
        for j in range(0,len(data)):
            if data[j][1][i]=='P':
                co+=1
        pres[1].append(co)
        
    data.append(pres)
    dict={
        'rows':data,
        'head_pop':header
    }
    table =get_template('table_grid/tgrid.html')
    table=table.render(dict)
    return HttpResponse(table);
    
    
    
def lecture(da,Class,subject):
    q=Q(subject=subject) & Q(Class=Class) & Q(date_time__lte=date(year=da.year,month=da.month,day=calendar.monthrange(da.year,da.month)[1])) & Q(date_time__gte=date(year=da.year,month=da.month,day=1))
    #subID=subject.objects.filter(name_iexact = subject).values_list('id',flat=True)[0]
    #ClassID = classes.objects.filter()
    q=q & Q(subject=subject)
    temp_time_list=[]
    lis_atten = attendance.objects.filter(q).values_list('date_time',flat=True)
    lis_atten=list(lis_atten)
    for time in lis_atten:
        time=time-timedelta(seconds=time.second,minutes=time.minute)
        if time not in temp_time_list:
            temp_time_list.append(time)
            
    return temp_time_list
    
@csrf_exempt   
def update(request):
    Date=datetime.strptime(request.POST['date'],'%Y-%m-%d %H:%M:%S')
    rollno=request.POST['rollno']
    status=request.POST['status'][0]
    Class=request.POST['Class'][0]
    sub=request.POST['subject'][0]
    
    
    if status=='A':
        q1=Q(entry_time__gte=Date) & Q(entry_time__lt=Date-timedelta(seconds=Date.second,minutes=Date.minute)+timedelta(hours=1))
        attendance.objects.filter(q1,student=studentprofile.objects.filter(roll_no=rollno)[0],Class=classes.objects.filter(id=Class)[0])[0].delete()
        return HttpResponse("Deleted")
    elif status=='P':
        obj = attendance()
        obj.date_time=Date-timedelta(minutes=Date.minute,seconds=Date.second)
        obj.entry_time=Date
        obj.Class=classes.objects.filter(id=Class)[0]
        obj.subject=subject.objects.filter(id=sub)[0]
        obj.student=studentprofile.objects.filter(roll_no=rollno)[0]
        obj.teacher=teacherprofile.objects.filter(user_id=STCrelation.objects.filter(Class=obj.Class,subject=obj.subject).values_list('teacher_id',flat=True)[0])[0]
        obj.save()
        return HttpResponse("Saved")
        
        
        
        