from django.shortcuts import render
from .models import User
import attendance_system.views as v
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render,HttpResponse
from attendance_system.err import err
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def Login(request):
    print(request.body)
    if request.method == "POST" : 
        user=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            login(request,user)
        
            if request.user.is_teacher:
                request.session["type_profile"]="teacher"
                return redirect('/teacher/dashboard/profile/'+str(request.user.pk)+'/')
            elif request.user.is_student:
                request.session["type_profile"]="student"
                return redirect('/student/dashboard/profile/'+str(request.user.pk)+'/')
            else:
                request.session["type_profile"]=""
                errors= [err(e="Only Teacher and Student can Login Here.Are You Staff Member go Here",link="/admin/"),err(e="IF NOT",link="/user/logout")]
                return render(request,'error.html',{'errors':errors})
        else:
            errors=[err(e="Enter Correct LOGIN Credentials",link="/")]
            return render(request,"error.html",{'errors':errors})
            
            
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

