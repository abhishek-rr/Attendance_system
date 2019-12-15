from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout,login,authenticate
from StudentProfile.models import StudentProfile
from django.core import serializers
from django.contrib.auth.models import User
from django.middleware.csrf import *

# Create your views here.
def Login(request):
    if request.method == 'POST':
        user=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            return redirect('/api/display/')
        else:
            return HttpResponse("ERROR:-Credentials are Incorrect")
    else:
        if request.session.is_empty():
            return render(request,'html/api_login_workThrough.html',{})
        authenticate(request)
        print('-------------------')
        print(request.user)
        return redirect('/api/display/')
        
def display(request):
    if request.method == 'GET':
        user    = User.objects.filter(pk = request.user.pk)[0]
        profile = StudentProfile.objects.filter(user = request.user.pk)[0]
        return HttpResponse(serializers.serialize('json',[user,profile])) 
        

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return HttpResponse("ERROR:-Error Logging Out")