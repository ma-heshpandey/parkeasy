from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserForm,UserFormForAdmin,UserUpdateForm
from .models import User
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from vehicle_info.models import Car,Bike,BikeTime,CarTime
from place_space.models import Space
from places.models import Places
from django.contrib.auth.decorators import login_required
from nepali.datetime import NepaliDateTime
from nepali.datetime import HumanizeDateTime
import pytz
from datetime import timedelta
from django.contrib import messages
# from django.views.generic.edit import UpdateView

# Create your views here.

@login_required(login_url='/login/')
def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']

            user_form = form.save()
            name1 = get_object_or_404(User, username=name)
            # return redirect('park:gmails',username=name)
            return redirect('user_detail:gmails')

    else:
        form = UserForm()
    return render(request, 'user_detail/registeration_form.html', {'form': form})



def sign_up_admin(request):
    if request.method == 'POST':
        form = UserFormForAdmin(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user_form = form.save()
            user_form.admin=True
            user_form.save()
            print('ma sign up vitra')
            name1 = get_object_or_404(User, username=name)
            user = authenticate(request, username=name, password=password)
            login(request,user)

            # return redirect('park:gmails',username=name)
            return redirect('user_detail:gmails')

    else:
        form = UserFormForAdmin()
    return render(request, 'user_detail/register_for_admin.html', {'form': form})






@login_required(login_url='/login/')
def send_mails(request):
    try:
        send_mail('You have succesffully register in Park Easy! Thank You',
                  'From Park-Easy Team',
                  'mahesh268paandey@gmail.com',
                  [request.user.email],fail_silently=False
                  )
        if request.user.admin is True:
            # return redirect('user_detail:admin_register_confirmation')
            return redirect('places:entry_of_place_by_admin')
        else:
            return redirect('places:place')
    except:
        if request.user.admin is True:
            return redirect('places:entry_of_place_by_admin')

            # return redirect('user_detail:admin_register_confirmation')
        else:
            # mmmmm
            return redirect('places:place')

def admin_register_confirmation(request):
    return render(request, 'user_detail/admin_request_confirmation.html')


class UserSignUp(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user_detail:gmails')
    success_message = "User created successfully"
    template_name = "user_detail/registeration_form.html"

    def form_valid(self, form):
        super(UserSignUp, self).form_valid(form)
        # The form is valid, automatically sign-in the user
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user == None:
            # User not validated for some reason, return standard form_valid() response
            return self.render_to_response(self.get_context_data(form=form))
        else:
            # Log the user in
            login(self.request, user)
            # Redirect to success url
            return HttpResponseRedirect(self.get_success_url())



def update_user(request):
    form=UserUpdateForm()
    if request.method=="POST":
        form=UserUpdateForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            mobile_number=form.cleaned_data['mobile_number']
            email=form.cleaned_data['email']
            request.user.first_name=first_name
            request.user.last_name=last_name
            request.user.mobile_number=mobile_number
            request.user.email=email
            print('')
            request.user.save()
            return redirect('user_detail:booking_detail_of_user')
        else:
            return render(request, 'user_detail/user_update_form.html', {'form': form})
    else:
        return render(request,'user_detail/user_update_form.html',{'form':form})
    # form=UserUpdateForm()
    # return


@login_required(login_url='/login/')
def booking_detail_of_user(request):


    bike_time_obj=request.user.bitime.all()   #bitime is related name of BikeTime
    car_time_obj=request.user.catime.all()    #catime is related_name of CarTime
    bike_time_obj=list(bike_time_obj)
    car_time_obj=list(car_time_obj)
    total_bike_booked=len(bike_time_obj)
    total_car_booked=len(car_time_obj)
    bike_list=[]
    car_list=[]
    can_delete_bike_space = False
    can_delete_car_space = False

    for i in range(total_bike_booked):
        can_delete_bike_space = False

        if bike_time_obj[i].related_bike.bike_in is False:
            can_delete_bike_space=True

        entering_time=bike_time_obj[i].entering_time
        entering_time=entering_time + timedelta(hours=6, minutes=15)
        # bike_list.append([i+1,NepaliDateTime.from_datetime(entering_time),bike_time_obj[i].leaving_time,bike_time_obj[i].related_place,
        #                  bike_time_obj[i].related_bike.bike_number,bike_time_obj[i].related_space])
        bike_list.append([i + 1, bike_time_obj[i].entering_time, bike_time_obj[i].leaving_time,
                      bike_time_obj[i].related_place,
                      bike_time_obj[i].related_bike.bike_number, bike_time_obj[i].related_space,bike_time_obj[i].pk,can_delete_bike_space,
                          bike_time_obj[i].related_place.place_link,
                          ])

    for i in range(total_car_booked):
        can_delete_car_space = False

        if car_time_obj[i].related_car.car_in is False:
            can_delete_car_space = True

        entering_time=car_time_obj[i].entering_time
        entering_time=entering_time + timedelta(hours=6, minutes=15)
        car_list.append([i+1,car_time_obj[i].entering_time,car_time_obj[i].leaving_time,car_time_obj[i].related_place,
                         car_time_obj[i].related_car.car_number,car_time_obj[i].related_space,car_time_obj[i].pk,can_delete_car_space
                         ,car_time_obj[i].related_place.place_link,])


    return render(request,'user_detail/show_booking_detail_of_user.html',{'can_delete_bike_space':can_delete_bike_space,'can_delete_car_space':can_delete_car_space,'bike_time_obj':bike_time_obj,'bike_list':bike_list,'car_list':car_list})


def delete_space_bike(request,pk_key):   #for bikes
    if BikeTime.objects.filter(pk=pk_key).exists():
        bike_time_object = BikeTime.objects.get(pk=pk_key)
        if bike_time_object.related_person==request.user and bike_time_object.related_bike.bike_in is False:
            if request.method=="POST":
                bike_obj=Bike.objects.get(user_name=bike_time_object.related_person,bike_number=bike_time_object.related_bike.bike_number)
                space_number=bike_time_object.related_space
                bike_time_obj_for_space=BikeTime.objects.filter(related_space=Space.objects.get(related_place=bike_time_object.related_place,space_number=space_number))
                bike_time_object.delete()
                bike_obj.delete()
                if len(bike_time_obj_for_space)==0:
                    space_obj=Space.objects.get(related_place=bike_time_object.related_place,space_number=space_number)
                    space_obj.empty=True
                    space_obj.partial_occupied=False
                    space_obj.occupied=False
                    space_obj.save()

                return redirect('user_detail:booking_detail_of_user')
            else:
                return render(request,'user_detail/confirmation_for_delete.html',{'pk_number':pk_key})
        else:
            return redirect('/')

    else:
        return redirect('/')



def delete_space_car(request,pk_key):   #for car
    if CarTime.objects.filter(pk=pk_key).exists():
        car_time_object = CarTime.objects.get(pk=pk_key)
        if car_time_object.related_person==request.user:
            if request.method=="POST":
                car_obj=Car.objects.get(user_name=car_time_object.related_person,car_number=car_time_object.related_car.car_number)
                space_number=car_time_object.related_space
                car_time_obj_for_space=CarTime.objects.filter(related_space=Space.objects.get(related_place=car_time_object.related_place,space_number=space_number))
                car_time_object.delete()
                car_obj.delete()
                if len(car_time_obj_for_space)==0:
                    space_obj=Space.objects.get(related_place=car_time_object.related_place,space_number=space_number)
                    space_obj.empty=True
                    space_obj.partial_occupied=False
                    space_obj.occupied=False
                    space_obj.save()

                return redirect('user_detail:booking_detail_of_user')
            else:
                return render(request,'user_detail/confirmation_for_delete.html',{'pk_number':pk_key})
    else:
        return redirect('/')





def change_the_vehicle_number(request,place_name,vehicle_number):
    if request.method=="POST":
        vehicle_number_to_change=request.POST.get('vehicle_number_to_change')

        if Bike.objects.filter(bike_number=vehicle_number).exists():
            bike_obj=Bike.objects.get(bike_number=vehicle_number)
            all_bike_obj=Bike.objects.all()
            for bike in all_bike_obj:
                print(bike.bike_number)
                print(vehicle_number_to_change)
                if bike.bike_number==vehicle_number_to_change:
                    messages.info(request, 'Vehicle Number is Already Present')
                    return redirect('user_detail:booking_detail_of_user')
            bike_obj.bike_number=vehicle_number_to_change
            bike_obj.save()
            messages.info(request, 'Vehicle Number Is Changed')
            return redirect('user_detail:booking_detail_of_user')
        elif Car.objects.filter(car_number=vehicle_number).exists():
            car_obj = Car.objects.get(car_number=vehicle_number)
            print(car_obj)
            all_car_obj = Car.objects.all()
            for car in all_car_obj:
                print(car.car_number)
                print(vehicle_number_to_change)
                if car.car_number == vehicle_number_to_change:
                    messages.info(request, 'Vehicle Number is Already Present')
                    return redirect('user_detail:booking_detail_of_user')
            car_obj.car_number = vehicle_number_to_change
            car_obj.save()
            messages.info(request, 'Vehicle Number Is Changed')
            return redirect('user_detail:booking_detail_of_user')
        else:
            return redirect('/')
    else:
         return redirect('/')



    print(place_name)
    print(vehicle_number)






# @login_required(login_url='/login/')
# def booking_detail_of_user(request):
#     vehicle=""
#     user_name=request.user
#     if Bike.objects.filter(user_name=user_name).exists():
#         vehicle='Motor Bike'
#         bike_obj=Bike.objects.get(user_name=user_name)
#         vehicle_number=bike_obj.bike_number
#         place_name=bike_obj.place
#
#         bike_time_object=BikeTime.objects.get(related_bike=bike_obj)
#         related_space=bike_time_object.related_space
#         entering_time=bike_time_object.entering_time
#         leaving_time=bike_time_object.leaving_time
#         return render(request,'user_detail/show_booking_detail_of_user.html',{'vehicle_number':vehicle_number,'related_space':related_space,'place_name':place_name,'vehicle':vehicle,'entering_time':entering_time,
#                                                                               'leaving_time':leaving_time})
#     else:
#         vehicle = 'Car'
#         car_obj = Car.objects.get(user_name=user_name)
#         vehicle_number = car_obj.car_number
#         place_name = car_obj.place
#         car_time_object = CarTime.objects.get(related_car=car_obj)
#         related_space=car_time_object.related_space
#         entering_time = car_time_object.entering_time
#         leaving_time = car_time_object.leaving_time
#         return render(request, 'user_detail/show_booking_detail_of_user.html',
#                       {'vehicle_number':vehicle_number,'place_name': place_name,'related_space':related_space, 'vehicle': vehicle, 'entering_time': entering_time,
#                        'leaving_time': leaving_time})
#
#
#
# def delete_user_details(request):
#     if Bike.objects.filter(user_name=request.user).exists():
#         place_name=Bike.objects.get(user_name=request.user).place
#         Bike.objects.get(user_name=request.user).delete()
#         spaces_obj=Space.objects.filter(related_place=place_name)
#         bike_time_obj=BikeTime.objects.filter(related_place=place_name)
#         places_obj = Places.objects.all()
#         for place in places_obj:
#             related_spaces = Space.objects.filter(related_place=place)  ##place sanga related space haru nikalyo
#             for each_space in related_spaces:  ###aba euta euta space ma kehi xa ke vanera check garne
#
#                 if each_space.bike_space is True:  ## yedi space bike space ho vane
#                     bike_time_obj_all = BikeTime.objects.filter(
#                         related_space=each_space)  ##biketime ma register vaye ko sabaii object nikalne related space ko
#                     if len(bike_time_obj_all) == 0:
#                         each_space.empty = True
#                         each_space.partial_occupied = False
#                         each_space.save()
#
#         return redirect('places:place')
#
#
#     else:
#         Car.objects.get(user_name=request.user).delete()
#
#         places_obj = Places.objects.all()
#         for place in places_obj:
#             related_spaces = Space.objects.filter(related_place=place)  ##place sanga related space haru nikalyo
#             for each_space in related_spaces:  ###aba euta euta space ma kehi xa ke vanera check garne
#
#                 if each_space.car_space is True:  ## yedi space bike space ho vane
#                     car_time_obj_all = CarTime.objects.filter(
#                         related_space=each_space)  ##biketime ma register vaye ko sabaii object nikalne related space ko
#                     if len(car_time_obj_all) == 0:
#                         each_space.empty = True
#                         each_space.partial_occupied = False
#                         each_space.save()
#         return redirect('places:place')
#


