from django import forms
from place_space.models import Space
from places.models import Places
Choices_baneshwor=[('C','Car'),('B','Bike')]

class PaymentForm(forms.Form):
    choose_vehicle = forms.ChoiceField(choices=Choices_baneshwor, widget=forms.RadioSelect)
    space_number = forms.IntegerField()
    place_name = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden', 'value': '{{place_name}}'}))

    def clean(self):
        space_related=self.cleaned_data['choose_vehicle']
        space_number=self.cleaned_data['space_number']
        place_name=self.cleaned_data['place_name']
        place_obj=Places.objects.get(name=place_name)
        if Space.objects.filter(related_place=Places.objects.get(name=place_name),space_number=space_related+str(space_number)).exists():
            pass
        else:
            raise forms.ValidationError('Space is not found')


class BaneshworSpace(forms.Form):
    choose_vehicle=forms.ChoiceField(choices=Choices_baneshwor,widget=forms.RadioSelect)
    space_number=forms.IntegerField()
    place_name=forms.CharField(widget=forms.TextInput(attrs={'type':'hidden','value':'{{place_name}}'}))

    def clean(self):
        space_related=self.cleaned_data['choose_vehicle']
        space_number=self.cleaned_data['space_number']
        place_name=self.cleaned_data['place_name']
        if Space.objects.filter(related_place=Places.objects.get(name=f'{place_name}'),space_number=space_related+str(space_number)).exists():
            pass
        else:
            raise forms.ValidationError('Space is not found')



Choices_tripureshwor=[('TC','Car'),('TB','Bike')]
class TripureshworSpace(BaneshworSpace):
    choose_vehicle=forms.ChoiceField(choices=Choices_tripureshwor,widget=forms.RadioSelect)

    def clean(self):
        super().clean()
