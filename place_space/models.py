from django.db import models

# Create your models here.
from django.db import models
from places.models import Places
# Create your models here.

class Space(models.Model):
    car_space=models.BooleanField(default=False)
    bike_space=models.BooleanField(default=False)
    related_place=models.ForeignKey(Places,on_delete=models.CASCADE,default=1)
    space_number=models.CharField(max_length=4)
    occupied=models.BooleanField(default=False)
    empty=models.BooleanField(default=True)
    partial_occupied=models.BooleanField(default=False)
    acess_to_space = models.IntegerField(default=0)

    def user_entry_for_space(self):
        self.acess_to_space = self.acess_to_space + 1
        self.save()

    def user_living_space(self):
        self.acess_to_space -= 1
        self.save()
    def __str__(self):
        return str(self.space_number)
