from django.db import models
from classes.models import classes,YEAR
from subject.models import subject
# Create your models here.
class year_sem_subject(models.Model):
    year = models.CharField(choices=YEAR,max_length=10)
    sem = models.PositiveSmallIntegerField(blank=True,null=True)
    sub = models.OneToOneField(subject,on_cascade=models.DELETE,null=True,blank=True)
    
    def __str__(self):
        return "This subject:-{} belongs to this Year:-{}  Sem:-{}".format(self.year,str(self.sem),sub)