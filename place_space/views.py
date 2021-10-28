from django.shortcuts import render, redirect, HttpResponse
from places.models import Places
from vehicle_info.models import Car, Bike, CarTime, BikeTime
from django.shortcuts import get_object_or_404
from .models import Space
from .forms import BaneshworParkingFirstEntry, BaneshworParkingSearchingEntry, BaneshworSearchingForm, \
    BaneshworParkingAdminFormFirstEntry, BaneshworParkingAdminSearchingEntry, BaneshworParkingFirstEntryForBookedSpace, \
    BaneshworParkingAdminFormFirstEntryForBookedSpace
from .forms import TripureshworParkingFirstEntry, TripureshworParkingSearchingEntry, TripureshworSearchingForm, \
    TripureshworParkingAdminFormFirstEntry, TripureshworParkingAdminSearchingEntry, \
    TripureshworParkingFirstEntryForBookedSpace, TripureshworParkingAdminFormFirstEntryForBookedSpace
from .forms import RegisterForm, RegisterFormForFirstEntry, RegisterFormForFirstEntryForBookedSpace, \
    RegisterFormForFirstEntryForBookedSpaceForadmin, RegsiterFormForFirstEntryForAdmin, RegisterFormForAdmin, \
    SearchingForm
from django.contrib.auth import get_user
from user_detail.models import User
from datetime import datetime, date, time, timedelta
from dateutil import parser
import pytz
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_function.models import AnonymousParkingUser
from nepali.datetime import NepaliDateTime
import nepali_datetime
import math
from django.db import transaction

# Create your views here.

form_dict_for_first_entry = {
    'Baneshwor Parking': BaneshworParkingFirstEntry,
    'Tripureshwor Parking': TripureshworParkingFirstEntry
}

form_dict_for_first_entry_for_booked_space = {
    'Baneshwor Parking': BaneshworParkingFirstEntryForBookedSpace,
    'Tripureshwor Parking': TripureshworParkingFirstEntryForBookedSpace
}

form_dict_for_searching = {
    'Baneshwor Parking': BaneshworSearchingForm,
    'Tripureshwor Parking': TripureshworSearchingForm
}

form_dict_after_search = {
    'Baneshwor Parking': BaneshworParkingSearchingEntry,
    'Tripureshwor Parking': TripureshworParkingSearchingEntry
}

admin_form_dict_for_first_entry = {
    'Baneshwor Parking': BaneshworParkingAdminFormFirstEntry,
    'Tripureshwor Parking': TripureshworParkingAdminFormFirstEntry
}

admin_form_dict_for_first_entry_for_booked_space = {
    'Baneshwor Parking': BaneshworParkingAdminFormFirstEntryForBookedSpace,
    'Tripureshwor Parking': TripureshworParkingAdminFormFirstEntryForBookedSpace
}

admin_form_dict_after_search = {
    'Baneshwor Parking': BaneshworParkingAdminSearchingEntry,
    'Tripureshwor Parking': TripureshworParkingAdminSearchingEntry
}


@login_required(login_url='/login/')
def show_the_space(request, name):
    if request.user.admin is True:
        if request.user.associated_place.name==name:
            pass
        else:
            return redirect('/')



    if request.user.admin is False or request.user.admin is True:
        vehicle = ""
        # vehicle_time_form=form_dict_for_searching[f'{name}']()
        vehicle_time_form = SearchingForm()
        place_obj = Places.objects.get(name=name)
        space_objects = Space.objects.filter(related_place=place_obj)
        space_objects_list = list(space_objects)
        bike_vacant_space_list = []
        car_vacant_space_list = []
        booked_space_list = []
        total_no_of_bike=0
        total_no_of_car=0
        first_entry = True  # to know for first entry

        for space in space_objects:
            if space.empty == True:
                if space.bike_space is True:
                    bike_vacant_space_list.append(space.space_number)
                if space.car_space is True:
                    car_vacant_space_list.append(space.space_number)
            if space.empty == False:
                booked_space_list.append(space.space_number)
            if space.car_space==True:
                total_no_of_car=total_no_of_car+1
                print(space.space_number+'car')
            else:
                print(space.space_number+'bike')
                total_no_of_bike=total_no_of_bike+1
        my_bookings=[]
        if BikeTime.objects.filter(related_person=request.user,related_place=place_obj).exists():
            bike_objects_for_user=BikeTime.objects.filter(related_person=request.user,related_place=place_obj)
            for bike in bike_objects_for_user:
                my_bookings.append(bike.related_space.space_number)

        if CarTime.objects.filter(related_person=request.user,related_place=place_obj).exists():
                    car_objects_for_user=CarTime.objects.filter(related_person=request.user,related_place=place_obj)
                    for car in car_objects_for_user:
                        my_bookings.append(car.related_space.space_number)




        # print(name)
        total_row_required_for_bike=math.ceil(total_no_of_bike)/9
        total_row_required_for_car=math.ceil(total_no_of_car)/4
        # print(total_no_of_car)
        # if Bike.objects.filter(user_name=request.user).exists():
        #     vehicle="Bike"
        # else:
        #     vehicle="Car"

        # register_form = RegisterFormForFirstEntry()
        # register_form = form_dict_for_first_entry[f'{name}']()
        register_form = RegisterFormForFirstEntry()
        # register_form_for_booked_space=form_dict_for_first_entry_for_booked_space[f'{name}']()
        register_form_for_booked_space = RegisterFormForFirstEntryForBookedSpace()
        print(bike_vacant_space_list)
        # print('hdiehi')


        if request.user.admin is False:
            return render(request, f'place_space/Show_view_of_place.html', {'register_form': register_form,
                                                                            'register_form_for_booked_space': register_form_for_booked_space,
                                                                            'car_vacant_space_list': car_vacant_space_list,
                                                                            'bike_vacant_space_list': bike_vacant_space_list,
                                                                            'vehicle': vehicle,
                                                                            'first_entry': first_entry,
                                                                            'place_name': name,
                                                                            'form': vehicle_time_form,
                                                                            'booked_space_list': booked_space_list,
                                                                            'total_no_of_bike':range(total_no_of_bike),
                                                                            'total_no_of_car':range(total_no_of_car),

                                                                            'place_obj':place_obj,
                                                                            'my_bookings': my_bookings,

                                                                            # 'place_obj_for_file':place_obj.display_text_file()
                                                                            })
        else:  # admin ko lagi sepearte form
            vehicle_time_form = SearchingForm()
            # register_form = admin_form_dict_for_first_entry[f'{name}']()
            register_form = RegsiterFormForFirstEntryForAdmin()
            # register_form_for_booked_space = admin_form_dict_for_first_entry_for_booked_space[f'{name}']
            register_form_for_booked_space = RegisterFormForFirstEntryForBookedSpaceForadmin()

            return render(request, f'place_space/Show_view_of_place.html', {'register_form': register_form,
                                                                            'register_form_for_booked_space': register_form_for_booked_space,
                                                                            'car_vacant_space_list': car_vacant_space_list,
                                                                            'bike_vacant_space_list': bike_vacant_space_list,
                                                                            'vehicle': vehicle,
                                                                            'first_entry': first_entry,
                                                                            'place_name': name,
                                                                            'form': vehicle_time_form,
                                                                            'booked_space_list': booked_space_list,
                                                                            'total_no_of_bike': range(total_no_of_bike),
                                                                            'total_no_of_car': range(total_no_of_car),
                                                                            'place_obj': place_obj,
                                                                            'my_bookings':my_bookings,
                                                                            })
            # return render(request,f'place_space/{name}_space.html',{'register_form':register_form,'register_form_for_booked_space':register_form_for_booked_space,'car_vacant_space_list':car_vacant_space_list,'bike_vacant_space_list':bike_vacant_space_list,'vehicle':vehicle,'first_entry':first_entry,'place_name':name,'form':vehicle_time_form,'booked_space_list':booked_space_list})


@transaction.atomic
def green_slots_entry(request, place_name):
    if request.method == "POST":
        # form=RegisterFormForFirstEntry(request.POST)
        if request.user.admin is False:
            # form = form_dict_for_first_entry[f'{place_name}'](request.POST)
            form = RegisterFormForFirstEntry(request.POST)
        else:
            # form = admin_form_dict_for_first_entry[f'{place_name}'](request.POST)
            form = RegsiterFormForFirstEntryForAdmin(request.POST)
        # form=form_dict_for_first_entry[f'{place_name}'](request.POST)
        if form.is_valid():
            space_number = form.cleaned_data['space_number']
            vehicle_number = form.cleaned_data['vehicle_number']
            booking_date = form.cleaned_data['booking_date']
            entering_time = form.cleaned_data['entering_time']
            leaving_time = form.cleaned_data['leaving_time']
            entering_time = datetime.combine(booking_date, entering_time)
            leaving_time = datetime.combine(booking_date, leaving_time)
            if Space.objects.filter(related_place=Places.objects.get(name=place_name),
                                    space_number=space_number).exists():
                space_obj = Space.objects.get(related_place=Places.objects.get(name=place_name),
                                              space_number=space_number)
                if space_obj.bike_space is True:
                    place_object = Places.objects.get(name=place_name)

                    if request.user.admin is True:
                        phone_number = form.cleaned_data['phone_number']
                        anonymous_person_name = form.cleaned_data['person_name']
                        bike_time_object = BikeTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = bike_time_object.confirm_the_space(vehicle_number,place_name)
                        if succed_or_fail is True:
                            AnonymousParkingUser.objects.create(vehicle_type='Bike',
                                                                vehicle_number=vehicle_number,
                                                                related_admin_of_place=request.user,
                                                                person_name=anonymous_person_name,
                                                                phone_number=phone_number)
                            return redirect('admin_function:list_of_task', place_name)
                        else:
                            return redirect('/')




                    else:
                        # bike_object=Bike(user_name=request.user,bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                        print('i am in')
                        bike_time_object = BikeTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = bike_time_object.confirm_the_space(vehicle_number,place_name)
                        if succed_or_fail is True:
                            return redirect('user_detail:booking_detail_of_user')
                        else:
                            messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                            return redirect('place_space:space',place_name)

                            # return render(request, 'place_space/Show_view_of_place.html', {'form': form})

                else:
                    place_object = Places.objects.get(name=place_name)

                    if request.user.admin is True:
                        phone_number = form.cleaned_data['phone_number']
                        anonymous_person_name = form.cleaned_data['person_name']
                        car_time_object = CarTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,
                                                                                    related_place=Places.objects.get(
                                                                                        name=place_name)))
                        succed_or_fail = car_time_object.confirm_the_space(vehicle_number, place_name)
                        if succed_or_fail is True:
                            AnonymousParkingUser.objects.create(vehicle_type='Bike',
                                                                vehicle_number=vehicle_number,
                                                                related_admin_of_place=request.user,
                                                                person_name=anonymous_person_name,
                                                                phone_number=phone_number)
                            return redirect('admin_function:list_of_task', place_name)
                        else:
                            return redirect('/')
                    else:
                        print('i am in')
                        car_time_object = CarTime(related_person=request.user,
                                                  related_place=place_object, entering_time=entering_time,
                                                  leaving_time=leaving_time,
                                                  related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = car_time_object.confirm_the_space(vehicle_number,place_name)
                        if succed_or_fail is True:
                            return redirect('user_detail:booking_detail_of_user')
                        else:
                            messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                            return redirect('place_space:space',place_name)

                            # return render(request, 'place_space/Show_view_of_place.html', {'form': form})

            else:
                return redirect('/')
        else:
            messages.info(request, 'Make Sure to put todays date and minimum of 30 minute booking time')

            return render(request, 'place_space/try.html', {'form': form})
    else:
        return redirect('/')



def booked_slots_entry(request, place_name):
    total_no_of_bike = 0
    total_no_of_car = 0
    space_objects = Space.objects.filter(related_place=Places.objects.get(name=place_name))
    for space in space_objects:

        if space.car_space == True:
            total_no_of_car = total_no_of_car + 1
        else:
            total_no_of_bike = total_no_of_bike + 1

    if request.method == "POST":
        # form=RegisterFormForFirstEntry(request.POST)
        if request.user.admin is False:
            # form = form_dict_for_first_entry_for_booked_space[f'{place_name}'](request.POST)
            form = RegisterFormForFirstEntryForBookedSpace(request.POST)
        else:
            # form = admin_form_dict_for_first_entry_for_booked_space[f'{place_name}'](request.POST)
            form = RegisterFormForFirstEntryForBookedSpaceForadmin(request.POST)
        # form=form_dict_for_first_entry[f'{place_name}'](request.POST)
        if form.is_valid():
            space_number = form.cleaned_data['space_number1']
            vehicle_number = form.cleaned_data['vehicle_number']
            booking_date = form.cleaned_data['booking_date']
            entering_time = form.cleaned_data['entering_time']
            leaving_time = form.cleaned_data['leaving_time']
            entering_time = datetime.combine(booking_date, entering_time)
            leaving_time = datetime.combine(booking_date, leaving_time)
            if Space.objects.filter(related_place=Places.objects.get(name=place_name),
                                    space_number=space_number).exists():
                space_obj = Space.objects.get(related_place=Places.objects.get(name=place_name),
                                              space_number=space_number)
                if space_obj.bike_space is True:
                    place_object = Places.objects.get(name=place_name)

                    if request.user.admin is True:
                        phone_number = form.cleaned_data['phone_number']
                        anonymous_person_name = form.cleaned_data['person_name']
                        bike_time_object = BikeTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = bike_time_object.can_book(vehicle_number=vehicle_number,place_name=place_name)
                        if succed_or_fail is True:

                            AnonymousParkingUser.objects.create(vehicle_type='Bike',
                                                                vehicle_number=vehicle_number,
                                                                related_admin_of_place=request.user,
                                                                person_name=anonymous_person_name,
                                                                phone_number=phone_number)
                            return redirect('admin_function:list_of_task', place_name)
                        else:
                            return redirect('/')




                    else:
                        # bike_object=Bike(user_name=request.user,bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                        print('i am in')
                        bike_time_object = BikeTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = bike_time_object.can_book(vehicle_number=vehicle_number,place_name=place_name)
                        if succed_or_fail is True:
                            return redirect('user_detail:booking_detail_of_user')
                        else:
                            messages.info(request,
                                          'Sorry,The Space For Your Time Is Already Booked. Check The Booked times before Choosing The Space')
                            return redirect('place_space:space', place_name)
                            # return redirect('/')
                else:
                    place_object = Places.objects.get(name=place_name)
                    if request.user.admin is True:
                        phone_number = form.cleaned_data['phone_number']
                        anonymous_person_name = form.cleaned_data['person_name']
                        car_time_object = CarTime(related_person=request.user,
                                                    related_place=place_object, entering_time=entering_time,
                                                    leaving_time=leaving_time,
                                                    related_space=Space.objects.get(space_number=space_number,
                                                                                    related_place=Places.objects.get(
                                                                                        name=place_name)))
                        succed_or_fail = car_time_object.can_book(vehicle_number=vehicle_number, place_name=place_name)
                        if succed_or_fail is True:

                            AnonymousParkingUser.objects.create(vehicle_type='Car',
                                                                vehicle_number=vehicle_number,
                                                                related_admin_of_place=request.user,
                                                                person_name=anonymous_person_name,
                                                                phone_number=phone_number)
                            return redirect('admin_function:list_of_task', place_name)
                        else:
                            return redirect('/')
                    else:
                        print('i am in')
                        car_time_object = CarTime(related_person=request.user,
                                                  related_place=place_object, entering_time=entering_time,
                                                  leaving_time=leaving_time,
                                                  related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                        succed_or_fail = car_time_object.can_book(vehicle_number=vehicle_number)
                        print(succed_or_fail)
                        if succed_or_fail is True:
                            return redirect('user_detail:booking_detail_of_user')
                        else:
                            messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                            return redirect('place_space:space', place_name)

                            return render(request, 'place_space/show_the_space', {'form': form})

            else:
                return redirect('/')
        else:
            return render(request, 'place_space/try.html', {'form': form})


def search_the_space(request, place_name):
    if (2 > 4):
        if request.method == "POST":
            form = form_dict_for_admin[f'{place_name}Admin'](request.POST)
            if form.is_valid():
                booking_date = form.cleaned_data['booking_date']
                entering_time = form.cleaned_data['entering_time']
                leaving_time = form.cleaned_data['leaving_time']
                anonymous_person_name = form.cleaned_data['person_name']
                phone_number = form.cleaned_data['phone_number']
                vehicle_type = form.cleaned_data['choice_field']
                vehicle_number = form.cleaned_data['vehicle_number']
                entering_time = datetime.combine(booking_date, entering_time)
                leaving_time = datetime.combine(booking_date, leaving_time)
                print(vehicle_type)

                if vehicle_type == 'bike':
                    # bike_object = Bike.objects.get(user_name=request.user)
                    place_object = Places.objects.get(name=place_name)
                    bike_object = Bike(user_name=request.user, bike_number=vehicle_number, place=place_object)

                    bike_time_object = BikeTime(related_bike=bike_object, related_person=request.user,
                                                related_place=place_object, entering_time=entering_time,
                                                leaving_time=leaving_time,
                                                )
                    available_space = bike_time_object.search_the_available_space()
                    if len(available_space) != 0:
                        available_space = list(available_space)
                        other_then_first = True
                        new_form = form_dict_for_admin[f'{place_name}Admin']()
                        leaving_time = str(leaving_time)
                        entering_time = str(entering_time)
                        register_form = RegisterForm()
                        return render(request, f'place_space/{place_name}_space.html',
                                      {'register_form': register_form, 'phone_number': phone_number,
                                       'anonymous_person_name': anonymous_person_name, 'vehicle_number': vehicle_number,
                                       'vehicle_type': vehicle_type, 'leaving_time': leaving_time,
                                       'entering_time': entering_time, 'form': new_form,
                                       'other_then_first': other_then_first, 'place_name': place_name,
                                       'available_space': available_space})

                    else:
                        messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                        return render(request, 'place_space/vehicle_time_form.html', {'form': form})
                else:
                    place_object = Places.objects.get(name=place_name)
                    car_object = Car(user_name=request.user, car_number=vehicle_number, place=place_object)

                    car_time_object = CarTime(related_car=car_object, related_person=request.user,
                                              related_place=place_object, entering_time=entering_time,
                                              leaving_time=leaving_time,
                                              )
                    available_space = car_time_object.search_the_available_space()
                    if len(available_space) != 0:
                        available_space = list(available_space)
                        other_then_first = True
                        new_form = form_dict_for_admin[f'{place_name}Admin']()
                        leaving_time = str(leaving_time)
                        entering_time = str(entering_time)

                        return render(request, f'place_space/{place_name}_space.html',
                                      {'phone_number': phone_number, 'anonymous_person_name': anonymous_person_name,
                                       'vehicle_number': vehicle_number,
                                       'vehicle_type': vehicle_type, 'leaving_time': leaving_time,
                                       'entering_time': entering_time, 'form': new_form,
                                       'other_then_first': other_then_first, 'place_name': place_name,
                                       'available_space': available_space})

                    else:
                        messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                        return render(request, 'place_space/vehicle_time_form.html', {'form': form})




            else:

                # vehicle_time_form = form_dict[f'{place_name}']()
                place_obj = Places.objects.get(name=place_name)
                space_objects = Space.objects.all()
                space_objects_list = list(space_objects)
                bike_vacant_space_list = []
                car_vacant_space_list = []
                booked_space_list = []
                first_entry = True  # to know for first entry
                for space in space_objects:
                    if space.empty == True:
                        if space.bike_space is True:
                            bike_vacant_space_list.append(space.space_number)
                        if space.car_space is True:
                            car_vacant_space_list.append(space.space_number)
                    if space.empty == False:
                        booked_space_list.append(space.space_number)
                    # vehicle_time_form = form_dict_for_admin[f'{place_name}Admin']()
                return render(request, f'place_space/{place_name}_space.html',
                              {'car_vacant_space_list': car_vacant_space_list,
                               'bike_vacant_space_list': bike_vacant_space_list,
                               'first_entry': first_entry, 'place_name': place_name, 'form': form,
                               'booked_space_list': booked_space_list})

                # return render(request, f'place_space/{place_name}_space.html',{'form': form})

        else:
            form = form_dict_for_admin[f'{place_name}Admin']()
            return render(request, 'place_space/vehicle_time_form.html', {'form': form})

    else:
        place_obj=Places.objects.get(name=place_name)
        if request.method == "POST":
            form = SearchingForm(request.POST)
            total_no_of_bike = 0
            total_no_of_car = 0
            space_objects = Space.objects.filter(related_place=Places.objects.get(name=place_name))
            for space in space_objects:

                if space.car_space == True:
                    total_no_of_car = total_no_of_car + 1
                else:
                    total_no_of_bike = total_no_of_bike + 1

            if form.is_valid():
                booking_date = form.cleaned_data['booking_date']
                entering_time = form.cleaned_data['entering_time']
                leaving_time = form.cleaned_data['leaving_time']
                vehicle_type = form.cleaned_data['choice_field']
                entering_time = datetime.combine(booking_date, entering_time)
                leaving_time = datetime.combine(booking_date, leaving_time)
                # if Bike.objects.filter(user_name=request.user).exists():
                # total_no_of_bike = 0
                # total_no_of_car = 0
                # space_objects=Space.objects.filter(related_place=Places.objects.get(name=place_name))
                # for space in space_objects:
                    # if space.empty == True:
                    #     if space.bike_space is True:
                    #         bike_vacant_space_list.append(space.space_number)
                    #     if space.car_space is True:
                    #         car_vacant_space_list.append(space.space_number)
                    # if space.empty == False:
                    #     booked_space_list.append(space.space_number)
                    # if space.car_space == True:
                    #     total_no_of_car = total_no_of_car + 1
                    # else:
                    #     total_no_of_bike = total_no_of_bike + 1
                if vehicle_type == 'bike':
                    # bike_object = Bike.objects.get(user_name=request.user)
                    place_object = Places.objects.get(name=place_name)
                    bike_time_object = BikeTime(related_person=request.user,
                                                related_place=place_object, entering_time=entering_time,
                                                leaving_time=leaving_time,
                                                )
                    print('############################')
                    available_space = bike_time_object.search_the_available_space()
                    if len(available_space) != 0:
                        available_space = list(available_space)
                        other_then_first = True
                        # new_form = form_dict_for_searching[f'{place_name}']()
                        new_form = SearchingForm()
                        leaving_time = str(leaving_time)
                        entering_time = str(entering_time)
                        if request.user.admin is False:
                            # register_form = form_dict_after_search[f'{place_name}']
                            register_form = RegisterForm()
                        else:
                            # register_form = admin_form_dict_after_search[f'{place_name}']
                            register_form = RegisterFormForAdmin()

                        return render(request, f'place_space/Show_view_of_place.html',
                                      {'register_form': register_form, 'leaving_time': leaving_time,
                                       'entering_time': entering_time,
                                       'form': new_form, 'other_then_first': other_then_first, 'place_name': place_name,
                                       'available_space': available_space,
                                       'total_no_of_car':range(total_no_of_car),
                                       'total_no_of_bike':range(total_no_of_bike),
                                       'place_obj': place_obj,
                                       })

                    else:
                        messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                        return render(request, 'place_space/vehicle_time_form.html', {'form': form})
                else:
                    # car_object = Car.objects.get(user_name=request.user)
                    place_object = Places.objects.get(name=place_name)
                    print('i am in')
                    car_time_object = CarTime(related_person=request.user,
                                              related_place=place_object, entering_time=entering_time,
                                              leaving_time=leaving_time
                                              )
                    available_space = car_time_object.search_the_available_space()
                    if len(available_space) != 0:
                        available_space = list(available_space)
                        other_then_first = True
                        # new_form = form_dict_for_searching[f'{place_name}']()
                        new_form = SearchingForm()
                        leaving_time = str(leaving_time)
                        entering_time = str(entering_time)
                        if request.user.admin is False:
                            # register_form = form_dict_after_search[f'{place_name}']
                            register_form = RegisterForm()
                        else:
                            # register_form = admin_form_dict_after_search[f'{place_name}']
                            register_form = RegisterFormForAdmin()
                        return render(request, f'place_space/Show_view_of_place.html',
                                      {'register_form': register_form, 'leaving_time': leaving_time,
                                       'entering_time': entering_time,
                                       'form': new_form, 'other_then_first': other_then_first,
                                       'place_name': place_name, 'available_space': available_space,
                                       'total_no_of_car':range(total_no_of_car),
                                       'total_no_of_bike':range(total_no_of_bike),
                                       'place_obj': place_obj,
                                       })

                    else:
                        messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
                        return render(request, 'place_space/vehicle_time_form.html', {'form': form})

            else:
                space_objects = Space.objects.filter(related_place=Places.objects.get(name=place_name))
                space_objects_list = list(space_objects)
                bike_vacant_space_list = []
                car_vacant_space_list = []
                booked_space_list = []
                first_entry = True  # to know for first entry
                for space in space_objects:
                    if space.empty == True:
                        if space.bike_space is True:
                            bike_vacant_space_list.append(space.space_number)
                        if space.car_space is True:
                            car_vacant_space_list.append(space.space_number)
                    if space.empty == False:
                        booked_space_list.append(space.space_number)
                # if Bike.objects.filter(user_name=request.user).exists():
                #     vehicle = "Bike"
                # else:
                #     vehicle = "Car"
                vehicle = ''
                return render(request, f'place_space/Show_view_of_place.html',
                              {'vehicle': vehicle, 'first_entry': first_entry, 'booked_space_list': booked_space_list,
                               'car_vacant_space_list': car_vacant_space_list, 'form': form, 'place_name': place_name,
                               'bike_vacant_space_list': bike_vacant_space_list,
                               'total_no_of_car': range(total_no_of_car),
                               'total_no_of_bike': range(total_no_of_bike)
                               })


def proceeded_after_user_searched(request, place_name):
    # def proceeded_after_user_searched(request,place_number,place_name,entering_time,leaving_time,vehicle_type='xyz',vehicle_number='123',anonymous_person='xyz',phone_number='xyz'):
    total_no_of_bike = 0
    total_no_of_car = 0
    space_objects = Space.objects.filter(related_place=Places.objects.get(name=place_name))
    for space in space_objects:

        if space.car_space == True:
            total_no_of_car = total_no_of_car + 1
        else:
            total_no_of_bike = total_no_of_bike + 1

    if request.method == 'POST':
        # form=form_dict_(request.POST)
        if request.user.admin is False:
            # form = form_dict_after_search[f'{place_name}'](request.POST)
            form = RegisterForm(request.POST)
        else:
            # form = admin_form_dict_after_search[f'{place_name}'](request.POST)
            form = RegisterFormForAdmin(request.POST)
        if form.is_valid():
            entering_time = form.cleaned_data['register_entering_time']
            leaving_time = form.cleaned_data['register_leaving_time']
            space_number = form.cleaned_data['space_number']
            vehicle_number = form.cleaned_data['vehicle_number']

            space_obj = Space.objects.get(space_number=space_number, related_place=Places.objects.get(name=place_name))
            if space_obj.bike_space is True:
                bike_time_object = BikeTime(related_person=request.user,
                                            related_place=Places.objects.get(name=place_name),
                                            entering_time=entering_time,
                                            leaving_time=leaving_time,
                                            related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                succed_or_fail = bike_time_object.can_book(vehicle_number=vehicle_number,place_name=place_name)
                if succed_or_fail is True:
                    if request.user.admin is True:
                        anonymous_person_name = form.cleaned_data['person_name']
                        phone_number = form.cleaned_data['phone_number']
                        AnonymousParkingUser.objects.create(vehicle_type='Bike', vehicle_number=vehicle_number,
                                                            related_admin_of_place=request.user,
                                                            person_name=anonymous_person_name,
                                                            phone_number=phone_number)
                        return redirect('admin_function:list_of_task', place_name)

                    return redirect('user_detail:booking_detail_of_user')
                else:
                    messages.info(request,'Be fast to book ')
                    return redirect('place_space:space', place_name)
            else:
                car_time_object = CarTime(related_person=request.user,
                                          related_place=Places.objects.get(name=place_name),
                                          entering_time=entering_time,
                                          leaving_time=leaving_time,
                                          related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
                succed_or_fail = car_time_object.can_book(vehicle_number=vehicle_number,place_name=place_name)
                if succed_or_fail is True:
                    if request.user.admin is True:
                        anonymous_person_name = form.cleaned_data['person_name']
                        phone_number = form.cleaned_data['phone_number']
                        AnonymousParkingUser.objects.create(vehicle_type='Car', vehicle_number=vehicle_number,
                                                            related_admin_of_place=request.user,
                                                            person_name=anonymous_person_name,
                                                            phone_number=phone_number)
                        return redirect('admin_function:list_of_task', place_name)

                    return redirect('user_detail:booking_detail_of_user')
                else:
                    messages.info(request,'Be fast to book ')
                    return redirect('place_space:space', place_name)
        else:
            messages.info(request,'Vehicle Number is already register')
            return redirect('place_space:space',place_name)
    # space_number=place_number
    # entering_time=datetime.strptime(str(entering_time),'%Y-%m-%d %H:%M:%S')
    # leaving_time=datetime.strptime(str(leaving_time),'%Y-%m-%d %H:%M:%S')
    #
    # if request.user.admin is True:
    #     place_object=Places.objects.get(name=place_name)
    #     if vehicle_type=='bike':
    #         bike_object=Bike(user_name=request.user,bike_number=vehicle_number,place=place_object)
    #         bike_time_object = BikeTime(related_bike=bike_object, related_person=request.user,
    #                                     related_place=place_object, entering_time=entering_time,
    #                                     leaving_time=leaving_time,
    #                                     related_space=Space.objects.get(space_number=space_number))
    #         succed_or_fail = bike_time_object.can_book(request.user.username,anonymous_person,vehicle_number,place_object.name)
    #         if succed_or_fail is True:
    #             AnonymousParkingUser.objects.create(vehicle_type=vehicle_type, vehicle_number=vehicle_number,
    #                                                 related_admin_of_place=request.user,
    #                                                 person_name=anonymous_person, phone_number=phone_number)
    #             return redirect('admin_function:list_of_task',place_name)
    #         else:
    #             form = form_dict[f'{place_name}']()
    #             messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book ')
    #             return render(request, 'place_space/vehicle_time_form.html', {'form': form})
    #     else:
    #         car_object = Car(user_name=request.user, car_number=vehicle_number, place=place_object)
    #         car_time_object = CarTime(related_car=car_object, related_person=request.user,
    #                                     related_place=place_object, entering_time=entering_time,
    #                                     leaving_time=leaving_time,
    #                                     related_space=Space.objects.get(space_number=space_number))
    #         succed_or_fail = car_time_object.can_book(request.user.username, anonymous_person, vehicle_number,
    #                                                    place_object.name)
    #         if succed_or_fail is True:
    #             AnonymousParkingUser.objects.create(vehicle_type=vehicle_type, vehicle_number=vehicle_number,
    #                                                 related_admin_of_place=request.user,
    #                                                 person_name=anonymous_person, phone_number=phone_number)
    #             return redirect('admin_function:list_of_task', place_name)
    #
    #
    #
    # else:
    #
    #
    #
    #     if Bike.objects.filter(user_name=request.user).exists():
    #         bike_object = Bike.objects.get(user_name=request.user)
    #         place_object = Places.objects.get(name=place_name)
    #         print('i am in')
    #         bike_time_object = BikeTime(related_bike=bike_object, related_person=request.user,
    #                                     related_place=place_object, entering_time=entering_time,
    #                                     leaving_time=leaving_time,
    #                                     related_space=Space.objects.get(space_number=space_number))
    #         succed_or_fail = bike_time_object.can_book()
    #         if succed_or_fail is True:
    #             return redirect('user_detail:booking_detail_of_user')
    #         else:
    #             form=form_dict[f'{place_name}']()
    #             messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
    #             return render(request, 'place_space/vehicle_time_form.html', {'form': form})
    #     else:
    #         car_object = Car.objects.get(user_name=request.user)
    #         place_object = Places.objects.get(name=place_name)
    #         car_time_object = CarTime(related_car=car_object, related_person=request.user,
    #                                     related_place=place_object, entering_time=entering_time,
    #                                     leaving_time=leaving_time,
    #                                     related_space=Space.objects.get(space_number=space_number))
    #         succed_or_fail = car_time_object.can_book()
    #         if succed_or_fail is True:
    #             return redirect('user_detail:booking_detail_of_user')
    #         else:
    #             form = form_dict[f'{place_name}']()
    #             messages.info(request, 'Sorry,The Place Is Booked Just Now!  Be Fast To Book')
    #             return render(request, 'place_space/vehicle_time_form.html', {'form': form})


def fetch_booked(request, space_number, place_name):
    space_obj = Space.objects.get(space_number=space_number, related_place=Places.objects.get(name=place_name))
    if space_obj.bike_space is True:
        bike_obj = BikeTime.objects.filter(related_space=space_obj)
        dic = {}

        bike_list = []
        for i in range(len(bike_obj)):
            print(bike_obj[i].leaving_time)
            time_taking_for_entering = ''
            time_taking_for_leaving = ''
            if bike_obj[i].entering_time.hour >= 12:
                time_taking_for_entering = 'pm'
            else:
                time_taking_for_entering = 'am'

            if bike_obj[i].leaving_time.hour >= 12:
                time_taking_for_leaving = 'pm'
            else:
                time_taking_for_leaving = 'am'

            # entering_time = bike_obj[i].entering_time + timedelta(hours=6, minutes=15)
            entering_time = bike_obj[i].entering_time
            leaving_time = bike_obj[i].leaving_time
            if entering_time.hour < 12:
                # entering_time = bike_obj[i].entering_time.time()
                pass
            else:
                entering_time = bike_obj[i].entering_time + timedelta(hours=6, minutes=15)
                entering_time = NepaliDateTime.from_datetime(entering_time)

            if leaving_time.hour < 12:
                # entering_time = bike_obj[i].entering_time.time()
                pass
            else:
                #
                leaving_time = bike_obj[i].leaving_time + timedelta(hours=6, minutes=15)
                leaving_time = NepaliDateTime.from_datetime(leaving_time)

            # entering_time.hour=entering_time.hour%12;

            # leaving_time=NepaliDateTime.from_datetime(leaving_time)
            print(entering_time.time().hour)
            print('testing is')
            print(bike_obj[i].entering_time)
            bike_list.append({'entering_time': str(entering_time.time()) + time_taking_for_entering,
                              'leaving_time': str(leaving_time.time()) + time_taking_for_leaving})
            # bike_list.append(str(bike_obj[i].entering_time.time()),str(bike_obj[i].leaving_time.time()))
        dic['bike'] = bike_list
        import json
        json_string = json.dumps(dic)
        print(json_string)

        return HttpResponse(json_string)

    else:
        car_obj = CarTime.objects.filter(related_space=space_obj)
        dic = {}

        car_list = []
        for i in range(len(car_obj)):
            print(car_obj[i].leaving_time)
            time_taking_for_entering = ''
            time_taking_for_leaving = ''
            if car_obj[i].entering_time.hour >= 12:
                time_taking_for_entering = 'pm'
            else:
                time_taking_for_entering = 'am'

            if car_obj[i].leaving_time.hour >= 12:
                time_taking_for_leaving = 'pm'
            else:
                time_taking_for_leaving = 'am'

            # entering_time = bike_obj[i].entering_time + timedelta(hours=6, minutes=15)
            entering_time = car_obj[i].entering_time
            leaving_time = car_obj[i].leaving_time
            if entering_time.hour < 12:
                # entering_time = bike_obj[i].entering_time.time()
                pass
            else:
                entering_time = car_obj[i].entering_time + timedelta(hours=6, minutes=15)
                entering_time = NepaliDateTime.from_datetime(entering_time)

            if leaving_time.hour < 12:
                # entering_time = bike_obj[i].entering_time.time()
                pass
            else:
                #
                leaving_time = car_obj[i].leaving_time + timedelta(hours=6, minutes=15)
                leaving_time = NepaliDateTime.from_datetime(leaving_time)

            # entering_time.hour=entering_time.hour%12;

            # leaving_time=NepaliDateTime.from_datetime(leaving_time)
            print(entering_time.time().hour)
            print('testing is')
            print(car_obj[i].entering_time)
            car_list.append({'entering_time': str(entering_time.time()) + time_taking_for_entering,
                             'leaving_time': str(leaving_time.time()) + time_taking_for_leaving})
            # bike_list.append(str(bike_obj[i].entering_time.time()),str(bike_obj[i].leaving_time.time()))
        dic['bike'] = car_list
        import json
        json_string = json.dumps(dic)
        print(json_string)

        return HttpResponse(json_string)




