from django import forms
from datetime import datetime,date,timedelta
from vehicle_info.models import Car,Bike
from dateutil import parser

CHOICES=[('car','Car'),('bike','Bike')]


class RestrictionOfVehicleNumberAndTime(forms.Form):
    pass

    def clean(self):
        date_received = self.cleaned_data.get('booking_date')
        entering_time_received = self.cleaned_data['entering_time']
        leaving_time_received = self.cleaned_data['leaving_time']
        print(entering_time_received)
        print(date_received)
        entering_date_time = datetime.combine(date_received, entering_time_received)
        leaving_date_time = datetime.combine(date_received, leaving_time_received)
        now_date = datetime.now()
        if (entering_date_time-now_date).total_seconds()<= 0:
            raise forms.ValidationError('Please dont enter past date and time')
        if (leaving_date_time<=entering_date_time):
            raise forms.ValidationError('Please dont enter past date and time')
        if (leaving_date_time-entering_date_time).total_seconds()<1800:
            print( (leaving_date_time-entering_date_time).total_seconds())
            raise forms.ValidationError('Minimum time for booking is 30 minute')
        if (now_date.date()!=entering_date_time.date()):
            print((leaving_date_time - entering_date_time).total_seconds())
            raise forms.ValidationError('Bookiong is done for today only')
        if (now_date.date()!=leaving_date_time.date()):
            raise forms.ValidationError('Bookiong is done for today only')


def check_the_duplicate_number_plate(value):
    if Car.objects.filter(car_number=value).exists():
        raise forms.ValidationError('Vehicle number already exit')
    if Bike.objects.filter(bike_number=value).exists():
        raise forms.ValidationError('Vehicle number already exit')


class RegisterForm(forms.Form):#search gaare paxi
    space_number = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'type': 'hidden'}))
    vehicle_number = forms.CharField(max_length=14,validators=[check_the_duplicate_number_plate], widget=forms.TextInput(attrs={}))
    register_entering_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))
    register_leaving_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

    def clean(self):
        super().clean()
        reg_ent = self.cleaned_data.get('register_entering_time')
        reg_leave = self.cleaned_data.get('register_leaving_time')
        ent_time_list = reg_ent.split('G')
        leaving_time_list = reg_leave.split('G')
        self.cleaned_data['register_entering_time'] = parser.parse(ent_time_list[0])
        self.cleaned_data['register_leaving_time'] = parser.parse(leaving_time_list[0])






class RegisterFormForFirstEntry(RestrictionOfVehicleNumberAndTime):
    space_number = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'type': 'hidden'}))
    vehicle_number = forms.CharField(max_length=14,validators=[check_the_duplicate_number_plate], widget=forms.TextInput(attrs={}))
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    entering_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    leaving_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean(self):
        super().clean()

class RegisterFormForFirstEntryForBookedSpace(RestrictionOfVehicleNumberAndTime):
    space_number1 = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'type': 'hidden'}))
    vehicle_number = forms.CharField(max_length=14,validators=[check_the_duplicate_number_plate], widget=forms.TextInput(attrs={}))
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    entering_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    leaving_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean(self):
        super().clean()

class RegisterFormForFirstEntryForBookedSpaceForadmin(RegisterFormForFirstEntryForBookedSpace,RestrictionOfVehicleNumberAndTime):
    phone_number = forms.CharField()
    person_name = forms.CharField()

class RegsiterFormForFirstEntryForAdmin(RegisterFormForFirstEntry,RestrictionOfVehicleNumberAndTime):
    vehicle_number = forms.CharField(max_length=255,validators=[check_the_duplicate_number_plate], widget=forms.TextInput(attrs={}))
    phone_number = forms.CharField(widget=forms.TimeInput(attrs={}))
    person_name = forms.CharField(widget=forms.TimeInput(attrs={}))

    def clean(self):
        super().clean()

class RegisterFormForAdmin(RegisterForm):
    person_name=forms.CharField(max_length=255, widget=forms.TextInput(attrs={}))
    phone_number=forms.CharField(max_length=255, widget=forms.TextInput(attrs={}))
    vehicle_number = forms.CharField(max_length=255,validators=[check_the_duplicate_number_plate], widget=forms.TextInput(attrs={}))

    def clean(self):
        super().clean()


class SearchingForm(RestrictionOfVehicleNumberAndTime):
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    entering_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time','class':'form-control'}))
    leaving_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','class':'form-control'}))
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Type of Vehicle')

    def clean(self):
        super().clean()

class BaneshworParkingSearchingEntry(RegisterForm):
    pass

    def clean(self):
        super().clean()

class TripureshworParkingSearchingEntry(RegisterForm):
    pass

    def clean(self):
        super().clean()


class BaneshworParkingFirstEntry(RegisterFormForFirstEntry):
    pass

    def clean(self):
        super().clean()

class TripureshworParkingFirstEntry(RegisterFormForFirstEntry):
    pass

    def clean(self):
        pass

class BaneshworParkingFirstEntryForBookedSpace(RegisterFormForFirstEntryForBookedSpace):
    pass

    def clean(self):
        super().clean()

class TripureshworParkingFirstEntryForBookedSpace(RegisterFormForFirstEntryForBookedSpace):
    pass



class BaneshworSearchingForm(SearchingForm):
    pass

    def clean(self):
        super().clean()

class TripureshworSearchingForm(SearchingForm):
    pass


class BaneshworParkingAdminFormFirstEntry(RegsiterFormForFirstEntryForAdmin):
    # vehicle_number = forms.CharField(max_length=255)
    # phone_number = forms.CharField()
    # person_name = forms.CharField()

    def clean(self):
        super().clean()
        # vehicle_number_received=self.cleaned_data.get('vehicle_number')
        # if Car.objects.filter(car_number=vehicle_number_received).exists():
        #     raise forms.ValidationError('Vehicle number already exit')
        # if Bike.objects.filter(bike_number=vehicle_number_received).exists():
        #     raise forms.ValidationError('Vehicle number already exit')
class TripureshworParkingAdminFormFirstEntry(RegsiterFormForFirstEntryForAdmin):
    # vehicle_number = forms.CharField(max_length=255)
    # phone_number = forms.CharField()
    # person_name = forms.CharField()

    def clean(self):
        super().clean()
        # vehicle_number_received=self.cleaned_data.get('vehicle_number')
        # if Car.objects.filter(car_number=vehicle_number_received).exists():
        #     raise forms.ValidationError('Vehicle number already exit')
        # if Bike.objects.filter(bike_number=vehicle_number_received).exists():
        #     raise forms.ValidationError('Vehicle number already exit')

class BaneshworParkingAdminFormFirstEntryForBookedSpace(RegisterFormForFirstEntryForBookedSpaceForadmin):

    def clean(self):
        super().clean()
        space_number = self.cleaned_data.get('space_number1')
        print(space_number)

class TripureshworParkingAdminFormFirstEntryForBookedSpace(RegisterFormForFirstEntryForBookedSpaceForadmin):

    def clean(self):
        space_number = self.cleaned_data.get('space_number1')
        print(space_number)

class BaneshworParkingAdminSearchingEntry(RegisterFormForAdmin):
    pass

class TripureshworParkingAdminSearchingEntry(RegisterFormForAdmin):
    pass

#################################################33   ##################################3  #######################################

####################################################   ##################################3  ########################################3








class BaneshworParkingTimeForm(forms.Form):
    booking_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    entering_time=forms.TimeField(widget=forms.TextInput(attrs={'type':'time'}))
    leaving_time=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label='Type of Vehicle')


    def clean(self):
        super().clean()
        date_received = self.cleaned_data.get('booking_date')
        entering_time_received=self.cleaned_data['entering_time']
        leaving_time_received=self.cleaned_data['leaving_time']
        entering_date_time=datetime.combine(date_received,entering_time_received)
        leaving_date_time = datetime.combine(date_received, leaving_time_received)
        now_date = datetime.now()

        # if (entering_date_time-now_date).total_seconds()<= 0:
        #     raise forms.ValidationError('Please dont enter past date and time')

        # if (entering_date_time.hour) <= 7 or (entering_date_time.hour) >= 17:
        #     raise forms.ValidationError('We are open from 7A.M to 5P.M')
        #
        # if leaving_date_time.hour <= 7 or leaving_date_time.hour >= 17:
        #     raise forms.ValidationError('We are open from 7A.M to 5P.M')

        # if (leaving_date_time - entering_date_time).total_seconds() <600:
        #     raise forms.ValidationError('Minimum time interval for space is 10 minutes')





class BaneshworParkingAdminForm(BaneshworParkingTimeForm):
    # booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # entering_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    # leaving_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    vehicle_number=forms.CharField(max_length=255)
    phone_number = forms.CharField()
    person_name = forms.CharField()
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label='Type of Vehicle')




    def clean(self):
        super().clean()
        vehicle_number_received=self.cleaned_data.get('vehicle_number')
        if Car.objects.filter(car_number=vehicle_number_received).exists():
            raise forms.ValidationError('Vehicle number already exit')
        if Bike.objects.filter(bike_number=vehicle_number_received).exists():
            raise forms.ValidationError('Vehicle number already exit')







class TripureshworParkingTimeForm(BaneshworParkingTimeForm):
    def clean(self):
        super().clean()
#     booking_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
#     entering_time=forms.TimeField(widget=forms.TextInput(attrs={'type':'time'}))
#     leaving_time=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
#
#
#     def clean(self):
#         super().clean()
#         date_received = self.cleaned_data.get('booking_date')
#         entering_time_received=self.cleaned_data['entering_time']
#         leaving_time_received=self.cleaned_data['leaving_time']
#         entering_date_time=datetime.combine(date_received,entering_time_received)
#         leaving_date_time = datetime.combine(date_received, leaving_time_received)
#         now_date = datetime.now()
#
#         if (entering_date_time-now_date).total_seconds()<= 0:
#             raise forms.ValidationError('Please dont enter past date and time')
#
#         # if (entering_date_time.hour) <= 7 or (entering_date_time.hour) >= 17:
#         #     raise forms.ValidationError('We are open from 7A.M to 5P.M')
#         #
#         # if leaving_date_time.hour <= 7 or leaving_date_time.hour >= 17:
#         #     raise forms.ValidationError('We are open from 7A.M to 5P.M')
#
#         if (leaving_date_time - entering_date_time).total_seconds() <600:
#             raise forms.ValidationError('Minimum time interval for space is 10 minutes')
#
#
#
#
# CHOICES=[('car','Car'),('bike','Bike')]

class TripureshworParkingAdminForm(BaneshworParkingAdminForm):
    # booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # entering_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    # leaving_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    # vehicle_number=forms.CharField(max_length=255)
    # phone_number = forms.CharField()
    # person_name = forms.CharField()
    # choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label='Type of Vehicle')
    #
    #
    #
    #
     def clean(self):
         super().clean()





