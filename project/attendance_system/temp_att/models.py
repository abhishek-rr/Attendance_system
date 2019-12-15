from django.db import models
from teacher.models import teacherprofile
from student.models import studentprofile
from subject.models import subject
from datetime import datetime 
from User.models import User
from classes.models import classes

# Create your models here.
        
class temp_attendance(models.Model):
    Class = models.ForeignKey(classes,on_delete=models.CASCADE,null=True,blank=True)
    User = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date_time = models.DateTimeField(blank=True,default=datetime.now,null=True)
    FLAG = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.date_time)
    