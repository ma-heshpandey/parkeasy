from vehicle_info.models import Car,Bike,CarTime,BikeTime
from places.models import Places
from datetime import datetime,timedelta
from user_detail.models import User
from place_space.models import Space
import pytz
from django.contrib.auth import get_user

#####look at place_space app config for applying this,and see in seetings and make changes in app of setting

def car_time_check():

    car_time_obj_all=CarTime.objects.all()
    for car_time in car_time_obj_all:

        entering_time=car_time.entering_time

        # correct_entering = entering_time + timedelta(hours=5, minutes=41)
        correct_entering=entering_time
        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        present_time=datetime.today()
        present_time=present_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        present_time=present_time+timedelta(minutes=0)
        print(correct_entering)
        print(present_time)
        diff_in_time=present_time-correct_entering

        ####look for 5 minute to come
        if diff_in_time.total_seconds()>900:
            car_owner=car_time.related_car

            # car_obj=Car.objects.get(user_name=User.objects.get(username=car_owner.user_name))
            if car_owner.car_in is False:
                if car_owner.user_name.admin is False:

                    car_owner.delete()

    bike_time_obj_all = BikeTime.objects.all()
    for bike_time in bike_time_obj_all:

        entering_time = bike_time.entering_time

        # correct_entering = entering_time + timedelta(hours=5, minutes=41)
        correct_entering = entering_time
        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        present_time = datetime.today()
        present_time = present_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        present_time = present_time + timedelta(minutes=0)
        print(correct_entering)
        print(present_time)
        diff_in_time = present_time - correct_entering

        ####look for 5 minute to come
        if diff_in_time.total_seconds() > 900:
            bike_owner = bike_time.related_bike

            # bike_obj = Bike.objects.get(user_name=User.objects.get(username=bike_owner.user_name))
            # if bike_obj.bike_in is False:
            #     bike_obj.delete()

            if bike_owner.bike_in is False:
                if bike_owner.user_name.admin is False:
                    bike_owner.delete()


    places_obj=Places.objects.all()

    for place in places_obj:
        related_spaces=Space.objects.filter(related_place=place)  ##place sanga related space haru nikalyo
        for each_space in related_spaces:                  ###aba euta euta space ma kehi xa ke vanera check garne
            if each_space.car_space is True:               ## yedi space car space ho vane
                car_time_obj_all=CarTime.objects.filter(related_space=each_space)  ##cartime ma register vaye ko sabaii object nikalne related space ko
                if len(car_time_obj_all)==0:
                    each_space.empty=True
                    each_space.partial_occupied=False
                    each_space.save()


            if each_space.bike_space is True:               ## yedi space bike space ho vane
                bike_time_obj_all=BikeTime.objects.filter(related_space=each_space)  ##biketime ma register vaye ko sabaii object nikalne related space ko
                if len(bike_time_obj_all)==0:
                    each_space.empty=True
                    each_space.partial_occupied=False
                    each_space.save()



# def bike_time_check():
#
#     bike_time_obj_all=BikeTime.objects.all()
#     for bike_time in bike_time_obj_all:
#
#         entering_time=bike_time.entering_time
#
#         # correct_entering = entering_time + timedelta(hours=5, minutes=41)
#         correct_entering=entering_time
#         correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
#         present_time=datetime.today()
#         present_time=present_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
#         present_time=present_time+timedelta(minutes=0)
#         print(correct_entering)
#         print(present_time)
#         diff_in_time=present_time-correct_entering
#
#         ####look for 5 minute to come
#         if diff_in_time.total_seconds()>300:
#             bike_owner=bike_time.related_car
#
#             bike_obj=Bike.objects.get(user_name=User.objects.get(username=bike_owner.user_name))
#             if bike_obj.bike_in is False:
#                 bike_obj.delete()
#
#
#     places_obj=Places.objects.all()
#
#     for place in places_obj:
#         related_spaces=Space.objects.filter(related_place=place)  ##place sanga related space haru nikalyo
#         for each_space in related_spaces:                  ###aba euta euta space ma kehi xa ke vanera check garne
#             if each_space.bike_space is True:               ## yedi space car space ho vane
#                 bike_time_obj_all=BikeTime.objects.filter(related_space=each_space)  ##cartime ma register vaye ko sabaii object nikalne related space ko
#                 if len(bike_time_obj_all)==0:
#                     each_space.empty=True
#                     each_space.partial_occupied=False
#                     each_space.save()
#
#
#             if each_space.bike_space is True:               ## yedi space bike space ho vane
#                 bike_time_obj_all=BikeTime.objects.filter(related_space=each_space)  ##biketime ma register vaye ko sabaii object nikalne related space ko
#                 if len(bike_time_obj_all)==0:
#                     each_space.empty=True
#                     each_space.partial_occupied=False
#                     each_space.save()

