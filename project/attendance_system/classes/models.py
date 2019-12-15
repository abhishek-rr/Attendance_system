from django.db import models

# Create your models here.
YEAR=(("FE","FE"),("SE","SE"),("TE","TE"),("BE","BE"),)

class classes(models.Model):
    year = models.CharField(choices=YEAR,max_length=10);
    division = models.PositiveSmallIntegerField(default=1);
    rollcall_start = models.CharField(default='000000',blank=True,max_length=6)
    rollcall_end = models.CharField(default='000999',blank=True,max_length=6)
    
    def __str__(self):
        return "{} {}".format(self.year,self.division)
    