from django.db import models
from datetime import datetime
from User.models import User
from subject.models import subject
from classes.models import classes

# Create your models here.
class studentprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    student_id=models.CharField(max_length=7,null=True, unique=False,blank=True, default='')
    image=models.ImageField(upload_to='profilepics/',blank=True,default='')
    mobile_number=models.BigIntegerField(blank=True,default=9999999999)
    parents_number=models.BigIntegerField(blank=True,default=9999999999)
    department=models.CharField(max_length=40,blank=True,default='')
    semester=models.PositiveSmallIntegerField(blank=True, null=True)
    dob=models.DateField(blank=True,default=datetime.now)
    address=models.CharField(max_length=100,blank=True,default='')
    roll_no=models.CharField(max_length=6,unique=False,blank=True)
    Class=models.ForeignKey(classes,on_delete=models.CASCADE,blank=True,null=True)
    batch=models.CharField(max_length=1,default='',blank=True)
    subject=models.ManyToManyField(subject,blank=True,null= True)
    RFID=models.CharField(max_length=8,blank=True,default='')
    
    def __str__(self):
        return "{}---{}".format(self.roll_no,self.user_id)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        