from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    student_id = models.CharField(max_length=7,null=False,unique=True,default='')
    profile_pic = models.ImageField(upload_to='profilepic/',null=False,default='')
    mobile_number=models.BigIntegerField(blank=True,default=9999999999)
    
    def __str__(self):
        return "{}".format(self.student_id)
        
    