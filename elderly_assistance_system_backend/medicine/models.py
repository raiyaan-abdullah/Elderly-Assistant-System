from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    time = models.TimeField()
    started = models.DateTimeField()
    drawer = models.PositiveIntegerField()
    
