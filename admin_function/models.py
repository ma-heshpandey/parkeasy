from django.db import models
from user_detail.models import User
from datetime import datetime
# Create your models here.

class AnonymousParkingUser(models.Model):
    related_admin_of_place=models.ForeignKey(User,on_delete=models.CASCADE)
    vehicle_type=models.CharField(max_length=255,default="vehicle")
    person_name=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=255)
    vehicle_number=models.CharField(max_length=255)

    def __str__(self):
        return self.person_name


class Payment(models.Model):
    payment_user=models.ForeignKey(User,on_delete=models.CASCADE)
    vehicle_type=models.CharField(max_length=25)
    vehicle_number=models.CharField(max_length=25)
    payment_date_time=models.DateTimeField(default=datetime.now)