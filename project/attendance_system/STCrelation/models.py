from django.db import models
from teacher.models import teacherprofile
from subject.models import subject
from classes.models import classes

# Create your models here.
class STCrelation(models.Model):
    teacher=models.ForeignKey(teacherprofile,on_delete=models.CASCADE)
    subject=models.ForeignKey(subject,on_delete=models.CASCADE)
    Class=models.ForeignKey(classes,on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}_Teaches_{}_ToClass_{}".format(self.teacher,self.subject,self.Class)