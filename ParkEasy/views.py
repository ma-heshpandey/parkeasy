from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect,get_object_or_404
from user_detail.models import User
from django.contrib.auth import get_user
from django.contrib import messages
#from vehicle_info.models import Car,Bike,BikeTime,CarTime


def  Home(request):
    return render(request,'home.html')

def contact_us(request):
    return render(request,'contact_us.html')


def admin_login(request):
    if request.method=="POST":
        name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            if user.is_staff is True:
                return redirect('admin_function:list_of_task')
            if user.admin is False:
                return redirect('/')
            if user.is_active is False:
                return redirect('/')
            else:
                login(request,user)
                return redirect('places:place')
        else:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'Either username or password mismatch')
                return render(request, 'user_login_form.html')
            else:
                messages.info(request, 'You are not registered! Please register')
                return render(request, 'user_login_form.html')

    else:
        return render(request,'admin_login_form.html')



def user_login(request):

    if request.method=="POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            print('ma login vitra chu')
            user = authenticate(request, username=name, password=password)
            print('i am in')
            if user is not None:
                if user.admin is True:
                    return redirect('/')
                else:

                    login(request, user)
                    person_user = get_user(request)
                    # # # ydi kasai le book garya cha vane direct booking bhaye ko show huncha
                    # time_obj = CarTime.objects.all()
                    # for obj in time_obj:
                    #     if obj.related_person == person_user:
                    #         space = obj.related_space
                    #         place = obj.related_place
                    #         return redirect('user_detail:booking_detail_of_user')
                    #
                    # person_user = get_user(request)
                    # time_obj = BikeTime.objects.all()
                    # for obj in time_obj:
                    #     if obj.related_person == person_user:
                    #         space = obj.related_space
                    #         place = obj.related_place
                    #         return redirect('user_detail:booking_detail_of_user')
                    # car_obj = Car.objects.all()
                    # # ##yedi kasai le car number enter garya cha vane direct place ma jancha
                    # for car in car_obj:
                    #     if car.user_name == person_user:
                    #         place = car.place
                    #         return redirect('place_space:space', place)
                    #
                    # bike_obj = Bike.objects.all()
                    # for bike in bike_obj:
                    #     if bike.user_name == person_user:
                    #         place = bike.place
                    #         return redirect('place_space:space', place)
                    #
                    return redirect('places:place')
            else:
                if User.objects.filter(username=name).exists():
                    messages.info(request,'Either username or password mismatch')
                    return render(request, 'user_login_form.html')
                else:
                    messages.info(request,'You are not registered! Please register')
                    return render(request, 'user_login_form.html')
    else:
        print('ma login vitra chu')
        return render(request,'user_login_form.html')


