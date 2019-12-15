import MySQLdb
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django import template
from rest_framework import viewsets
from User.models import User
from .serializer import UserSerializer

def homepageview(request,errors=None):
    print(request.GET)
    print("__________________________________________________")
    print(request.META)
    print("__________________________________________________")
    print(request.body)
    return render(request,'HomePage.html',{'errors':errors})
    
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
