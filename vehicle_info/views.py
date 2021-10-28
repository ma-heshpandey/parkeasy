from django.shortcuts import render,redirect,get_object_or_404
from .models import Car,Bike
from places.models import Places
from .forms import CarForm,BikeForm
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse

# Create your views here.
@login_required(login_url='/login/')
def car_register(request,name):
    if request.method=="POST":
        particular_user = get_user(request)

        car_number = request.POST['car_number']

        car_objects = Car.objects.all()
        for car in car_objects:
            if car.car_number == car_number:
                messages.info(request, 'Warning : vehicle number already exists')
                car = 'car'
                return render(request, 'places/map_of_place.html',
                              {'name': name, 'car': car})

        place_name = get_object_or_404(Places, name=name)

        Car.objects.create(user_name=particular_user, car_number=car_number, place=place_name)
        return redirect('place_space:space', name)



@login_required(login_url='/login/')
def bike_register(request,name):
    if request.method=="POST":

        particular_user = get_user(request)

        bike_number=request.POST['bike_number']

        bike_objects=Bike.objects.all()
        for bikes in bike_objects:
            if bikes.bike_number==bike_number:
                messages.info(request,'Warning : vehicle number already exists')
                bike='bike'
                return render(request, 'places/map_of_place.html',
                              {'name': name,'bike':bike})

        place_name=get_object_or_404(Places,name=name)
        Bike.objects.create(user_name=particular_user,bike_number=bike_number,place=place_name)
        return redirect('place_space:space',name)






# @login_required(login_url='/login/')
# def vehicle_status(request,name):
#     if request.method=='POST':
#         vehicle_number=request.POST.get('vehicle_number')
#         vehicle_type=request.POST.get('vehicle_type')
#         print(vehicle_number)
#         if vehicle_type=='car':
#             car_obj_all = Car.objects.all()
#             car_number_got = ''
#             new_car_number = ''
#             count_word = 0
#             for char in vehicle_number:
#
#                 if char != ' ':
#                     if count_word == 0:
#                         car_number_got = char
#                         count_word += 1
#                         print(car_number_got)
#                     else:
#                         car_number_got = car_number_got + char
#
#             for car_obj in car_obj_all:
#                 count_word = 0
#                 for char in car_obj.car_number:
#                     if char != ' ':
#                         if count_word == 0:
#                             new_car_number = char
#                             count_word += 1
#                         else:
#                             new_car_number = new_car_number + char
#
#
#                 if new_car_number.lower() == car_number_got.lower():
#                     car_obj.car_in = True
#                     car_obj.save()
#                     return redirect('place_space:space', car_obj.place)
#                 else:
#                     messages.info(request,'Car doesnt exit')
#                     return redirect('place_space:space',name)
#         else:
#             if vehicle_type == 'bike':
#                 bike_obj_all =Bike.objects.all()
#                 bike_number_got = ''
#                 new_bike_number = ''
#                 count_word = 0
#                 for char in vehicle_number:
#
#                     if char != ' ':
#                         if count_word == 0:
#                             bike_number_got = char
#                             count_word += 1
#                             print(bike_number_got)
#                         else:
#                             bike_number_got = bike_number_got + char
#
#                 for bike_obj in bike_obj_all:
#                     count_word = 0
#                     for char in bike_obj.bike_number:
#                         if char != ' ':
#                             if count_word == 0:
#                                 new_bike_number = char
#                                 count_word += 1
#                             else:
#                                 new_bike_number = new_bike_number + char
#
#                     if new_bike_number.lower() == bike_number_got.lower():
#                         bike_obj.bike_in = True
#                         bike_obj.save()
#                         return redirect('place_space:space', bike_obj.place)
#                     else:
#                         messages.info(request, 'Bike doesnt exit')
#                         return redirect('place_space:space', name)
#
#     else:
#         return render(request,'vehicle_info/check_in.html')


def check_in(request,number):
    print(number)
    bike_obj=Bike.objects.filter(bike_number=number)
    if len(bike_obj)>0:
        for bike in bike_obj:
            bike.bike_in=True
            print('jiji')
            bike.save()

    car_obj = Car.objects.filter(car_number=number)
    if len(car_obj) > 0:
        for car in car_obj:
            car.car_in = True
            print('jiji')
            car.save()




    return JsonResponse({'success':True})

