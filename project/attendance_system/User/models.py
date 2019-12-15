#from teacher.models import create_teacherprofile

from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_teacher=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    
    def __str__(self):
        return "{}".format(self.username)
        
