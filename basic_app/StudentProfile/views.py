from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout,login,authenticate
from .models import StudentProfile
from django.core import serializers
from django.contrib.auth.models import User

# Create your views here.
def Login(request):
    if request.method == 'POST':
        user=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            return redirect('/display')
        else:
            return HttpResponse("Credentials are Incorrect")
    else:
        return render(request,'html/login.html',{})
        
def display(request):
    if request.method == 'GET':
        user    = User.objects.filter(pk = request.user.pk)[0]
        profile = StudentProfile.objects.filter(user = request.user.pk)[0]
        return render(request,'html/display.html',{'user':user,'profile':profile})
        
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return HttpResponse("ERROR:Error Logging Out")