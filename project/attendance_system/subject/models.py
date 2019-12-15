from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class subject(models.Model):
    name = models.CharField(max_length=50,null=False)
    code   = models.IntegerField(unique=True,null=False)
    semester = models.PositiveSmallIntegerField(default=1,validators=[MaxValueValidator(8),MinValueValidator(1)])
    
    def __str__(self):
        return self.name