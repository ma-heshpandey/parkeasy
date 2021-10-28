from django import forms
from . import models
class PlacesFormToRegister(forms.ModelForm):
    class Meta():
        model=models.Places
        # fields='__all__'
        fields=['name','location','number_of_car_space','number_of_bike_space','place_link']

        widgets={
            'name': forms.TextInput(attrs={'placeholder': 'Place Name', 'class':"form-control",}),
            'location': forms.TextInput(attrs={'placeholder': 'Location', 'class':"form-control",}),
            'number_of_car_space': forms.NumberInput(attrs={'placeholder': '10', 'class':"form-control",}),
            'number_of_bike_space': forms.NumberInput(attrs={'placeholder': '10', 'class':"form-control",}),
            'place_link': forms.TextInput(attrs={'placeholder': 'https://google.maps.com', 'class':"form-control",}),
        }