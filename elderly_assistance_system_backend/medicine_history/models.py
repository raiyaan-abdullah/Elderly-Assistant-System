from django.db import models

# Create your models here.
class MedicineHistory(models.Model):
    medicine_id = models.IntegerField(default=0)
    date = models.DateField() 
    consumed = models.BooleanField()
    time_of_consumption = models.TimeField()
