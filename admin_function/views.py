from django.shortcuts import render,redirect,HttpResponse
from vehicle_info.models import BikeTime,CarTime,Bike,Car
from place_space.models import Space
from places.models import Places
from user_detail.models import User
from .models import AnonymousParkingUser,Payment
from django.contrib.auth.decorators import login_required
from .forms import BaneshworSpace,TripureshworSpace,PaymentForm
from datetime import timedelta,datetime
from nepali.datetime import NepaliDateTime
from dateutil.parser import parse
# Create your views here.

payment_form_of_places={'Baneshwor Parking':BaneshworSpace,
              'Tripureshwor Parking':TripureshworSpace
              }
space_list_of_bike_of_all_places=['B','TB']
space_list_of_car_of_all_places=['C','TB']
# Create your views here.



@login_required(login_url='/login/')
def list_of_task(request,place_name):
    # payment_form=payment_form_of_places[f'{place_name}']()
    payment_form=PaymentForm()
    place_obj=Places.objects.get(name=place_name)
    bike_object=Bike.objects.filter(place=place_obj)
    vehicle_list_detail=[]
    list_of_vehicle_number=[]


    if request.user.admin is True:
        if request.user.associated_place.name==place_name:
            pass
        else:
            redirect('/')

    for individual_bike_obj in bike_object:
        if individual_bike_obj.user_name.admin is False:
            if individual_bike_obj.bike_in is False:
                owner=individual_bike_obj.user_name
                vehicle_number=individual_bike_obj.bike_number
                vehicle='Bike'

                if BikeTime.objects.filter(related_bike=individual_bike_obj).exists():
                    bike_time=BikeTime.objects.get(related_bike=individual_bike_obj)
                    space_number = bike_time.related_space
                    list_of_vehicle_number.append(vehicle_number)
                    #vehicle_list_detail.append(('<button>Name: '+str(owner)+'</button>','<button>Vehicle No: '+str(vehicle_number)+'</button>'+'  | ','<button>'+vehicle+'</button>',str(space_number)))
                    vehicle_list_detail.append(
                        (  f''' <table class="table table-bordered">
                              <thead>
                                <tr>
                                  <th scope="col">{owner}</th>''',f'''
                                  <th scope="col">{vehicle_number}</th>''',f''' 
                                  <th scope="col">{vehicle}</th>
                                </tr>
                              </thead>''',space_number

                        )
                    )


    car_object = Car.objects.filter(place=place_obj)
    for individual_car_obj in car_object:
        if individual_car_obj.user_name.admin is False:
            if individual_car_obj.car_in is False:
                owner = individual_car_obj.user_name
                vehicle_number = individual_car_obj.car_number
                vehicle = 'Car'
                if CarTime.objects.filter(related_car=individual_car_obj).exists():
                    car_time = CarTime.objects.get(related_car=individual_car_obj)
                    space_number = car_time.related_space
                    list_of_vehicle_number.append(vehicle_number)
                    #vehicle_list_detail.append(('Name: '+str(owner),'Vehicle No: '+str(vehicle_number),vehicle,space_number))
                    vehicle_list_detail.append(
                        (f''' <table class="table table-bordered">
                                                  <thead>
                                                    <tr>
                                                      <th scope="col">{owner}</th>''', f'''
                                                      <th scope="col">{vehicle_number}</th>''', f''' 
                                                      <th scope="col">{vehicle}</th>
                                                    </tr>
                                                  </thead>''', space_number

                         )
                    )

    list_of_bike_to_present_in_table=[]
    list_of_bike_to_present_in_table_for_admin=[]
    list_of_all_bike=Bike.objects.filter(place=place_obj)
    for individual_bike in list_of_all_bike:
        if individual_bike.user_name.admin is False:
            space_obj_of_individuals=BikeTime.objects.get(related_bike=individual_bike)
            list_of_bike_to_present_in_table.append((str(individual_bike.user_name.first_name+' '+individual_bike.user_name.last_name),individual_bike.bike_number,space_obj_of_individuals.related_space,'Bike'))
        else:
            space_obj_of_individuals=BikeTime.objects.get(related_bike=individual_bike)
            not_register_user=AnonymousParkingUser.objects.get(vehicle_number=individual_bike.bike_number)
            list_of_bike_to_present_in_table_for_admin.append((str(not_register_user.person_name),individual_bike.bike_number,space_obj_of_individuals.related_space,'Bike'))


    list_of_car_to_present_in_table=[]
    list_of_car_to_present_in_table_for_admin=[]
    list_of_all_car=Car.objects.filter(place=place_obj)
    for individual_car in list_of_all_car:
        if individual_car.user_name.admin is False:
            space_obj_of_individuals=CarTime.objects.get(related_car=individual_car)
            list_of_car_to_present_in_table.append((str(individual_car.user_name.first_name+' '+individual_car.user_name.last_name),individual_car.car_number,space_obj_of_individuals.related_space,'Car'))
        else:
            space_obj_of_individuals=CarTime.objects.get(related_car=individual_car)
            not_register_user=AnonymousParkingUser.objects.get(vehicle_number=individual_car.car_number)
            list_of_car_to_present_in_table_for_admin.append((str(not_register_user.person_name),individual_car.car_number,space_obj_of_individuals.related_space,'Car'))






    return render(request,'admin_function/admin_all_function_page.html',{'list_of_car_to_present_in_table_for_admin':list_of_car_to_present_in_table_for_admin,'list_of_bike_to_present_in_table_for_admin':list_of_bike_to_present_in_table_for_admin,'list_of_car_to_present_in_table':list_of_car_to_present_in_table,'list_of_bike_to_present_in_table':list_of_bike_to_present_in_table,'list_of_vehicle_number':list_of_vehicle_number,'payment_form':payment_form,'vehicle_list_detail':vehicle_list_detail,'place_name':place_name})



@login_required(login_url='/login/')
def payment(request,place_name):
    if request.method=="POST":
        # form=payment_form_of_places[f'{place_name}'](request.POST)
        form=PaymentForm(request.POST)
        if form.is_valid():


            space_number=form.cleaned_data['space_number']
            space_related=form.cleaned_data['choose_vehicle']
            print(space_number)
            print(space_related)
            print(place_name)
            # if space_related=='B':
            if space_related in space_list_of_bike_of_all_places:

                space_obj = Space.objects.get(related_place=Places.objects.get(name=place_name),space_number=space_related+str(space_number))
                bike_time_obj=BikeTime.objects.filter(related_space=space_obj)
                if len(bike_time_obj)>0:
                    print(bike_time_obj)
                    li = []
                    li_for_admin=[]
                    for bike_time in bike_time_obj:
                        bike_related_name = bike_time.related_person
                        #print(type(bike_related_name))
                        #user_name = User.objects.get(username=bike_related_name)
                        user_name = bike_related_name
                        if user_name.admin is False:
                            # bike = Bike.objects.get(user_name=user_name)
                            bike=bike_time.related_bike
                            bike_person=user_name.get_full_name()
                            li.append((bike_person, bike.bike_number))
                        else:
                            user_objects = Bike.objects.filter(user_name=user_name,place=Places.objects.get(name=place_name))
                            user_objects=list(user_objects)
                            for user in user_objects:
                                if user.user_name.admin is True:
                                    anonymous_user_associated=AnonymousParkingUser.objects.all()
                                    bike_number_of_anonymous=user.bike_number
                                    for all_user in anonymous_user_associated:
                                        if all_user.vehicle_number==bike_number_of_anonymous:
                                            print(all_user.person_name,user.bike_number)
                                            li_for_admin.append((all_user.person_name,user.bike_number,'Admin'))
                                break

                    print(li)
                    print(li_for_admin)
                    dic = {'vehicle_list':li,'vehicle_list_for_admin': li_for_admin, 'space_number': space_obj.space_number,'place_name':place_name}
                    return render(request, 'admin_function/list_of_people.html', context=dic)
                else:
                    return redirect('admin_function:list_of_task',place_name)

            else:
                space_obj = Space.objects.get(related_place=Places.objects.get(name=place_name),
                                              space_number=space_related + str(space_number))
                car_time_obj = CarTime.objects.filter(related_space=space_obj)
                print(car_time_obj)
                li = []
                li_for_admin = []
                if len(car_time_obj)>0:
                    for car_time in car_time_obj:
                        car_related_name = car_time.related_person
                        print(car_related_name)
                        user_name = User.objects.get(username=car_related_name)
                        if user_name.admin is False:
                            # car = Car.objects.get(user_name=user_name)
                            car=car_time.related_car
                            car_person = user_name.get_full_name()
                            li.append((car_person, car.car_number))
                        else:

                            user_objects = Car.objects.filter(user_name=user_name,place=Places.objects.get(name=place_name))
                            user_objects = list(user_objects)

                            for user in user_objects:
                                if user.user_name.admin is True:
                                    anonymous_user_associated = AnonymousParkingUser.objects.all()
                                    car_number_of_anonymous = user.car_number

                                    for all_user in anonymous_user_associated:

                                        if all_user.vehicle_number == car_number_of_anonymous:

                                            li_for_admin.append((all_user.person_name, user.car_number,'Admin'))
                                break

                    print(li_for_admin)
                    dic = {'vehicle_list': li, 'space_number': space_obj.space_number,'vehicle_list_for_admin': li_for_admin,'place_name':place_name}
                    return render(request, 'admin_function/list_of_people.html', context=dic)
                else:
                    return redirect('admin_function:list_of_task', place_name)
        else:
            return redirect('admin_function:list_of_task',place_name)



@login_required(login_url='/login/')
def display_payment(request,name,vehicle_number,space_number,place_name,booked_by='xyz'):
    space_obj = Space.objects.get(space_number=space_number, related_place=Places.objects.get(name=place_name))

    if request.method=="POST":
        if request.method == "POST":
            if space_obj.car_space is True:
                car_obj = Car.objects.get(car_number=vehicle_number)
                payment_obj=Payment(payment_user=car_obj.user_name,vehicle_type='Car',vehicle_number=car_obj.car_number)
                payment_obj.save()
                car_obj.delete()
                if AnonymousParkingUser.objects.filter(vehicle_number=vehicle_number).exists():
                    anonymous_car_obj = AnonymousParkingUser.objects.get(vehicle_number=vehicle_number)
                    anonymous_car_obj.delete()

                car_time_obj = CarTime.objects.filter(related_space=space_obj)
                if len(car_time_obj) == 0:
                    space_obj.empty = True
                    space_obj.partial_occupied = False
                    space_obj.save()

                return redirect('admin_function:list_of_task', place_name)
            else:
                if space_obj.bike_space is True:
                    bike_obj = Bike.objects.get(bike_number=vehicle_number)
                    payment_obj = Payment(payment_user=bike_obj.user_name, vehicle_type='Bike',
                                          vehicle_number=bike_obj.bike_number)
                    payment_obj.save()
                    bike_obj.delete()
                    if AnonymousParkingUser.objects.filter(vehicle_number=vehicle_number).exists():
                        anonymous_bike_obj = AnonymousParkingUser.objects.get(vehicle_number=vehicle_number)
                        anonymous_bike_obj.delete()


                    bike_time_obj = BikeTime.objects.filter(related_space=space_obj,related_place=Places.objects.get(name=place_name))
                    if len(bike_time_obj) == 0:
                        space_obj.empty = True
                        space_obj.partial_occupied = False
                        space_obj.save()


                    return redirect('admin_function:list_of_task', place_name)

    else:
        space_obj = Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name))
        if space_obj.bike_space is True:
            bike_obj=Bike.objects.get(bike_number=vehicle_number)
            biketime_obj=BikeTime.objects.get(related_bike=bike_obj)
            # time_in_hour=biketime_obj.payment()
            # total_cost=time_in_hour[0]*30
            # print(time_in_hour)
            # print(type(time_in_hour))
            # if time_in_hour[1]:
            #     extra_time_in_minutes = time_in_hour[1]
            #     extra_money = extra_time_in_minutes * 20

            list_of_time = biketime_obj.payment()
            total_cost = list_of_time[0] * 30
            print(list_of_time)
            print(type(list_of_time))
            extra_time_in_minutes=0
            extra_money=0
            grand_total_cost=0
            if list_of_time[1]>=300:
                extra_time_in_minutes = list_of_time[1]
                extra_money = extra_time_in_minutes * 20
                grand_total_cost=extra_money+total_cost

            if booked_by=='xyz':
                vehicle='Bike' #template ma bike ke car separate garna lai
                dic={'grand_total_cost':round(grand_total_cost),'extra_time_in_minutes':round(extra_time_in_minutes),'extra_money':round(extra_money),'time':round(list_of_time[0],2),'vehicle':vehicle,'cost':round(total_cost),'Entered':biketime_obj.entering_time,'Leaving':biketime_obj.leaving_time,'name':name,'vehicle_number':vehicle_number}
            else:
                vehicle = 'Bike'  # template ma bike ke car separate garna lai
                dic = {'grand_total_cost':round(grand_total_cost),'extra_time_in_minutes':round(extra_time_in_minutes),'extra_money':round(extra_money),'booked_by':booked_by,'time': round(list_of_time[0],2), 'vehicle': vehicle, 'cost': total_cost, 'Entered': biketime_obj.entering_time,
                       'Leaving': biketime_obj.leaving_time, 'name': name, 'vehicle_number': vehicle_number}

            return render(request,'admin_function/payment_detail.html',context=dic)

        else:
            car_obj = Car.objects.get(car_number=vehicle_number)
            cartime_obj = CarTime.objects.get(related_car=car_obj)
            list_of_time = cartime_obj.payment()
            total_cost = list_of_time[0] * 30

            print(list_of_time)
            print(type(list_of_time))
            extra_time_in_minutes = 0
            extra_money = 0
            grand_total_cost = 0
            if list_of_time[1]>=300:

                extra_time_in_minutes = list_of_time[1]
                extra_money = extra_time_in_minutes * 20
                grand_total_cost = extra_money + total_cost


            if booked_by == 'xyz':
                vehicle = 'Car'  # template ma bike ke car separate garna lai
                dic = {'grand_total_cost':round(grand_total_cost),'extra_time_in_minutes':round(extra_time_in_minutes),'extra_money':round(extra_money),'time': list_of_time[0], 'vehicle': vehicle, 'cost': round(total_cost), 'Entered': cartime_obj.entering_time,
                       'Leaving': cartime_obj.leaving_time, 'name': name, 'vehicle_number': vehicle_number}
            else:
                vehicle = 'Car'  # template ma bike ke car separate garna lai
                dic = {'booked_by': booked_by, 'time': list_of_time[0], 'vehicle': vehicle, 'cost': total_cost,
                       'Entered': cartime_obj.entering_time,
                       'Leaving': cartime_obj.leaving_time, 'name': name, 'vehicle_number': vehicle_number}

            return render(request, 'admin_function/payment_detail.html', context=dic)



def fetch_booked_to_show_for_admin(request,space_number,place_name):

    if Space.objects.filter(space_number=space_number.upper(),related_place=Places.objects.get(name=place_name)).exists():
        space_obj=Space.objects.get(space_number=space_number.upper(),related_place=Places.objects.get(name=place_name))
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
                entering_time=bike_obj[i].entering_time
                leaving_time=bike_obj[i].leaving_time
                booked_by=''
                if bike_obj[i].related_person.admin is False:
                    booked_for=''
                else:
                    anonymous_user_obj=AnonymousParkingUser.objects.get(vehicle_number=bike_obj[i].related_bike.bike_number)
                    booked_for= anonymous_user_obj.person_name

                bike_list.append({'UserName':str(bike_obj[i].related_person),'FullName':bike_obj[i].related_person.get_full_name(),
'entering_time': str(entering_time.date())+' '+str(entering_time.time())+time_taking_for_entering ,
                                  'leaving_time': str(leaving_time.date())+' '+str(leaving_time.time())+time_taking_for_leaving,'vehicle_number':bike_obj[i].related_bike.bike_number,'space_number':space_obj.space_number,'booked_for':booked_for})
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
                entering_time = car_obj[i].entering_time
                leaving_time = car_obj[i].leaving_time
                booked_by = ''
                if car_obj[i].related_person.admin is False:
                    booked_for = ''
                else:
                    anonymous_user_obj = AnonymousParkingUser.objects.get(
                        vehicle_number=car_obj[i].related_car.car_number)
                    booked_for = anonymous_user_obj.person_name

                car_list.append({'UserName': str(car_obj[i].related_person),
                                 'FullName':car_obj[i].related_person.get_full_name(),
                                  'entering_time': str(entering_time.date()) + ' ' + str(
                                      entering_time.time()) + time_taking_for_entering,
                                  'leaving_time': str(leaving_time.date()) + ' ' + str(
                                      leaving_time.time()) + time_taking_for_leaving,
                                  'vehicle_number': car_obj[i].related_car.car_number,'space_number':space_obj.space_number,'booked_for':booked_for})
                # bike_list.append(str(bike_obj[i].entering_time.time()),str(bike_obj[i].leaving_time.time()))
            dic['bike'] = car_list
            import json
            json_string = json.dumps(dic)
            print(json_string)

            return HttpResponse(json_string)

def delete_space_by_admin(request,vehicle_number,space_number,place_name):
    if Space.objects.filter(space_number=space_number.upper(),related_place=Places.objects.get(name=place_name)).exists():
        space_obj=Space.objects.get(space_number=space_number.upper(), related_place=Places.objects.get(name=place_name))
        if space_obj.bike_space is True:
            bike_obj=Bike.objects.get(bike_number=vehicle_number)
            bike_obj.delete()

            bike_time_obj=BikeTime.objects.filter(related_space=space_obj,related_place=Places.objects.get(name=place_name))
            if len(bike_time_obj)==0:
                space_obj.empty=True
                space_obj.partial_occupied=False
                space_obj.save()



        else:
            car_obj = Car.objects.get(car_number=vehicle_number)
            car_obj.delete()

            car_time_obj = CarTime.objects.filter(related_space=space_obj,
                                                    related_place=Places.objects.get(name=place_name))
            if len(car_time_obj) == 0:
                space_obj.empty = True
                space_obj.partial_occupied = False
                space_obj.save()

        return redirect('admin_function:list_of_task',place_name)



def manage_the_space(request,vehicle_number,space_number,place_name,user_name):
    if request.method=="POST":
        changed_space_number=request.POST.get('space_number_to_change')
        space_number=request.POST.get('space_number')
        vehicle_type=request.POST.get('vehicle_type')
        # transfer_to=request.POST.get('transfer_to')
        entering_time=request.POST.get('entering_time')
        increase_time=request.POST.get('increase_time')
        print(increase_time)

        entering_time=parse(entering_time)

        print(type(entering_time))

        leaving_time=request.POST.get('leaving_time')
        leaving_time=parse(leaving_time)

        owner_name=request.POST.get('owner_name')
        time_obj=datetime.now().time()
        total_minutes_to_add_in_time=0
        # user ko entering time ma ,syatem bata update hun alye ko time plus update vaye paxi ko 5 minute add hunxa
        if increase_time=="on":
            total_minutes_to_add_in_time=(datetime.now()+timedelta(minutes=0))-(entering_time+timedelta(minutes=0))+timedelta(minutes=5)
            total_minutes_to_add_in_time=total_minutes_to_add_in_time.total_seconds()/60
        # total_minutes_to_add_in_leaving_time=(datetime.now()+timedelta(minutes=0))-(leaving_time+timedelta(minutes=0))+timedelta(minutes=5)
        # total_minutes_to_add_in_leaving_time=total_minutes_to_add_in_leaving_time.total_seconds()/60



        if vehicle_type=="Car":
            car_time_obj=CarTime.objects.filter(related_space=Space.objects.get(space_number=space_number,related_place=Places.objects.get(name=place_name)))
            for car_time in car_time_obj:
                print(car_time.entering_time.date())
                print(car_time.entering_time.time().minute)

                print(entering_time.date())
                print(entering_time.time().minute)
                print(total_minutes_to_add_in_time)

                # print(leaving_time.time())
                print(changed_space_number)
                if car_time.entering_time.date()==entering_time.date()  and car_time.entering_time.time().minute==entering_time.time().minute and car_time.leaving_time.date()==leaving_time.date()  and car_time.leaving_time.time().minute==leaving_time.time().minute and car_time.leaving_time.time().hour==leaving_time.time().hour:
                    car_time.related_space=Space.objects.get(space_number=changed_space_number,related_place=Places.objects.get(name=place_name))
                    car_time.entering_time=car_time.entering_time+timedelta(minutes=total_minutes_to_add_in_time)
                    car_time.leaving_time=car_time.leaving_time+timedelta(minutes=total_minutes_to_add_in_time)
                    car_time.related_car.car_in=True
                    car_time.related_car.save()
                    car_time.save()



                    changed_space_obj=Space.objects.get(space_number=changed_space_number,related_place=Places.objects.get(name=place_name))
                    changed_space_obj.empty=False
                    changed_space_obj.partial_occupied=True
                    changed_space_obj.save()
                    space_obj=Space.objects.get(space_number=space_number, related_place=Places.objects.get(name=place_name))
                    car_obj_in_that_space=CarTime.objects.filter(related_space=space_obj)
                    if len(car_obj_in_that_space)==0:
                        space_obj.empty=True
                        space_obj.partial_occupied=False
                        space_obj.save()

                    return redirect('admin_function:list_of_task',place_name)

        else:
            bike_time_obj = BikeTime.objects.filter(related_space=Space.objects.get(space_number=space_number,
                                                                                  related_place=Places.objects.get(
                                                                                      name=place_name)))
            for bike_time in bike_time_obj:
                print(bike_time.entering_time.date())
                print(entering_time.date())
                print(changed_space_number)
                if bike_time.entering_time.date() == entering_time.date() and bike_time.entering_time.time().minute == entering_time.time().minute and bike_time.leaving_time.date() == leaving_time.date() and bike_time.leaving_time.time().minute == leaving_time.time().minute and bike_time.leaving_time.time().hour == leaving_time.time().hour:
                    bike_time.related_space = Space.objects.get(space_number=changed_space_number,
                                                               related_place=Places.objects.get(name=place_name))
                    bike_time.entering_time = bike_time.entering_time + timedelta(minutes=total_minutes_to_add_in_time)
                    bike_time.leaving_time = bike_time.leaving_time + timedelta(minutes=total_minutes_to_add_in_time)
                    bike_time.related_bike.bike_in = True
                    bike_time.related_bike.save()
                    bike_time.save()




                    changed_space_obj = Space.objects.get(space_number=changed_space_number,
                                                          related_place=Places.objects.get(name=place_name))
                    changed_space_obj.empty = False
                    changed_space_obj.partial_occupied = True
                    changed_space_obj.save()
                    space_obj = Space.objects.get(space_number=space_number,
                                                  related_place=Places.objects.get(name=place_name))
                    bike_obj_in_that_space = BikeTime.objects.filter(related_space=space_obj)
                    if len(bike_obj_in_that_space) == 0:
                        space_obj.empty = True
                        space_obj.partial_occupied = False
                        space_obj.save()

                    return redirect('admin_function:list_of_task', place_name)


    else:
        type_of_vehicle=''
        if Bike.objects.filter(place=Places.objects.get(name=place_name),bike_number=vehicle_number).exists():
            bike=Bike.objects.get(place=Places.objects.get(name=place_name), bike_number=vehicle_number)
            print(bike)
            bike_obj=BikeTime.objects.get(related_bike=bike)

            type_of_vehicle='Bike'
            entering_time=bike_obj.entering_time
            leaving_time=bike_obj.leaving_time
            owner=bike_obj.related_person.get_full_name()
            space_number=bike_obj.related_space.space_number
            all_bike_user_for_that_place=Bike.objects.filter(place=Places.objects.get(name=place_name))

            list_of_all_user = User.objects.all()
            # for bike in all_bike_user_for_that_place:
            #     for list in list_of_all_bike_user:
            #         if list != bike.user_name.username:
            #             list_of_all_bike_user.append(bike.user_name.username)
            if bike_obj.related_person.admin is True:
                anonymous_user=AnonymousParkingUser.objects.get(vehicle_number=vehicle_number)

                context = {'list_of_all_user':list_of_all_user,'user_name':user_name,'vehicle_type': type_of_vehicle, 'entering_time': entering_time, 'leaving_time': leaving_time,
                           'owner': anonymous_user, 'space_number': space_number,'booked_by':'Admin','vehicle_number':vehicle_number}
            else:

                context={'list_of_all_user':list_of_all_user,'user_name':user_name,'vehicle_type':type_of_vehicle,'entering_time':entering_time,'leaving_time':leaving_time,
                         'owner':owner,'space_number':space_number,'vehicle_number':vehicle_number }
            return render(request,'admin_function/manage_the_space.html',context)

        else:
            car = Car.objects.get(place=Places.objects.get(name=place_name), car_number=vehicle_number)
            print(car)
            car_obj = CarTime.objects.get(related_car=car)

            type_of_vehicle = 'Car'
            entering_time = car_obj.entering_time
            leaving_time = car_obj.leaving_time
            owner = car_obj.related_person.get_full_name()
            space_number = car_obj.related_space.space_number
            # all_car_user_for_that_place=Car.objects.filter(place=Places.objects.get(name=place_name))
            list_of_all_car_user=[]
            list_of_all_user=User.objects.all()
            # for car in all_car_user_for_that_place:
            #     for list in list_of_all_car_user:
            #         if list!=car.user_name.username:
            #             list_of_all_car_user.append(car.user_name.username)
            #
            # print(list_of_all_car_user)

            if car_obj.related_person.admin is True:
                anonymous_user = AnonymousParkingUser.objects.get(vehicle_number=vehicle_number)

                context = {'user_name':user_name,'vehicle_type': type_of_vehicle, 'entering_time': entering_time, 'leaving_time': leaving_time,'list_of_all_user':list_of_all_user,
                           'owner': anonymous_user, 'space_number': space_number, 'booked_by': 'Admin','vehicle_number':vehicle_number}
            else:

                context = {'user_name':user_name,'vehicle_type': type_of_vehicle, 'entering_time': entering_time, 'leaving_time': leaving_time,'list_of_all_user':list_of_all_user,
                           'owner': owner, 'space_number': space_number,'vehicle_number':vehicle_number}
            return render(request, 'admin_function/manage_the_space.html', context)