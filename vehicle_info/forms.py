from django import forms
from .models import Car,Bike


class CarForm(forms.ModelForm):
    class Meta:
        model=Car
        fields=['car_number',]


class BikeForm(forms.ModelForm):
    class Meta:
        model=Bike
        fields=['bike_number',]
