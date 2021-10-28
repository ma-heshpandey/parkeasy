from django.contrib import admin
from .models import CarTime,Car,Bike,BikeTime
# Register your models here.

admin.site.register(Car)
admin.site.register(CarTime)
admin.site.register(BikeTime)
admin.site.register(Bike)