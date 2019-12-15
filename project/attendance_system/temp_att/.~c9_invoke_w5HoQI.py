from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import temp_attendance
from django.views.decorators.csrf import csrf_exempt
from classes.models import classes
from teacher.models import teacherprofile
from student.models import studentprofile
from datetime import datetime
# Create your views here.
@csrf_exempt
def save(request):
    RFID=request.POST['RFID']
    Class=request.POST['Class'][0]
    FLAG=request.POST['FLAG']
    obj= temp_attendance()
    if FLAG==1:
        teacher_id=teacherprofile.objects.get(RFID=RFID).values_list('user_id',flat=True)
        if not teacher_id:
            pass
        else:
            obj.User = User.objects.get(pk=teacher_id)
            obj.FLAG = True
            obj.Class = Class
            obj.save()
    elif FLAG==0:
        student_id=studentprofile.objects.get(RFID=RFID).values_list('user_id',flat=True)
        if not student_id:
            pass
        else:
            obj.User = User.objects.get(pk=student_id)
            obj.FLAG =False
            obj.Class = Class
            obj.save()
    else:
        print("Something Wrong with Card!!!")
    return HttpResponse("Added")
    
def Apply(request):
    RFID=request.POST['RFID']
    Class=request.POST['Class']
    FLAG=request.POST['FLAG']
    obj= temp_attendance()
    if FLAG==1:
        teacher_id = teacherprofile.objects.get()
        temp_attendance.objects.filter(User=teacher_id,Class=)