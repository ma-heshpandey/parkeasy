from django.db import models
from user_detail.models import User
from django.shortcuts import render,redirect,get_object_or_404

# Create your models here.

class Places(models.Model):
    associate_admin=models.OneToOneField(User,on_delete=models.CASCADE,default=1,related_name='associated_place')
    name=models.CharField(max_length=256)
    location=models.CharField(max_length=256)
    total_space=models.IntegerField(default=10)
    remaining_space=models.IntegerField(default=10)
    occupied_space=models.IntegerField(default=0)
    available_space=models.IntegerField(default=10)
    number_of_bike_space=models.IntegerField(default=10)
    number_of_car_space=models.IntegerField(default=10)
    place_overview_file=models.FileField(upload_to='documents/',null=True,blank=True)
    place_link=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

    def display_text_file(self):

        # with open(self.place_overview_file.path) as fp :
        with open(self.place_overview_file.path,'r') as fp, open(f'templates/{self.name}.html','w') as html_file :
        #     return fp.read()
            for line in fp:
                # append content to second file
                html_file.write(line)

            # return html_file

        # with open(f'templates/{self.name}.html') as fp :



        return self.name

    def remain_space(self):
        self.remaining_space=self.total_space-self.occupied_space
        self.available_space=self.remaining_space
        self.save()

    def occupied_plus(self):
        self.occupied_space+=1
        self.save()

    def occupied_minus(self):
        self.occupied_space-=1
        self.save()

