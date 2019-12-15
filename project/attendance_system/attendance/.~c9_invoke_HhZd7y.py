from django.db import models
from teacher.models import teacherprofile
from student.models import studentprofile
from subject.models import subject
from datetime import datetime
from User.models import User
from classes.models import classes

# Create your models here.
class attendance(models.Model):
    date_time = models.DateTimeField(blank=True,default = datetime.now)
    status = models.CharField(max_length=1,choices=(('P','PRESENT'),('A','ABSENT')),default='A')
    entry_time = models.DateTimeField(blank=True,default = datetime.now)
    teacher = models.ForeignKey(teacherprofile,on_delete=models.CASCADE)
    student = models.ForeignKey(studentprofile,on_delete=models.CASCADE)
    subject = models.ForeignKey(subject,on_delete=models.CASCADE)
    Class = models.ForeignKey(classes,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return "{0} {1} {2} {3}".format(self.date_time,self.status,self.entry_time,self.teacher.teacher_id)
        
        
class temp_atte
    Class = models.ForeignKey(classes,on_delete=)