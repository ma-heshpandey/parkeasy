from django.db import models
from user_detail.models import User
from places.models import Places
from place_space.models import Space
from datetime import datetime,time,date,timedelta,timezone
import time as time_for_sleep
import pytz
from django.db import transaction

# Create your models here.

class Car(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    car_number=models.CharField(max_length=20,null=False)
    place=models.ForeignKey(Places,on_delete=models.CASCADE,default=1)
    car_in=models.BooleanField(default=False)
    booked_date_and_time=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.user_name)


class Bike(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_number = models.CharField(max_length=20, null=False)
    place = models.ForeignKey(Places, on_delete=models.CASCADE, default=1)
    bike_in = models.BooleanField(default=False)
    booked_date_and_time=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user_name)




class CarTime(models.Model):
    related_car=models.ForeignKey(Car,on_delete=models.CASCADE,default=1)
    related_person=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='catime')
    related_place=models.ForeignKey(Places,on_delete=models.CASCADE,default=1)
    related_space=models.ForeignKey(Space,on_delete=models.CASCADE,default=1)
    entering_time=models.DateTimeField()
    leaving_time=models.DateTimeField()


    def __str__(self):
        return str(self.related_space)

    @transaction.atomic
    def confirm_the_space(self,vehicle_number,place_name):
        related_place = self.related_place
        car_obj = Car(user_name=self.related_person, car_number=vehicle_number,
                      place=self.related_place)

        space_object_for_permission = Space.objects.select_for_update().get(space_number=self.related_space.space_number,
                                                                            related_place=self.related_place)


        if space_object_for_permission.acess_to_space == 0:
            space_object_for_permission.acess_to_space += 1
            space_object_for_permission.save()
        else:
            return False

        if len(CarTime.objects.filter(related_space=self.related_space,related_place=related_place))>0:
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return False

        else:
            car_objs = Car.objects.all()
            for car in car_objs:
                if car.car_number == car_obj.car_number:
                    space_object_for_permission.acess_to_space -= 1
                    space_object_for_permission.save()
                    return False

            car_obj.save()
            self.related_car=car_obj




            self.save()
            # space_object_for_permission.acess_to_space -= 1
            # space_object_for_permission.save()

            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            space_obj=Space.objects.get(space_number=self.related_space,related_place=related_place)

            space_obj.empty = False
            space_obj.partial_occupied = True
            space_obj.save()
            return True

    def search_the_available_space(self):
        related_place = self.related_place
        available_set = set()
        space_obj = Space.objects.filter(related_place=related_place)
        print(space_obj)
        for obj in space_obj:
            if obj.car_space is True:
                time_obj = CarTime.objects.filter(related_space=obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        print(correct_entering)
                        print("above this is entering time of database")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        # correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        # correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=5)
                        correct_leaving += timedelta(minutes=5)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('UTC'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('UTC'))
                        aune = (self.entering_time + timedelta(minutes=0))
                        # print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            print('you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('you can save')
                        else:
                            print('i am wrong')
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        print(available_set,"this is available set")
        return available_set

    @transaction.atomic
    def can_book(self,asociated_user='xyz',anonymous_person_name='xyz',vehicle_number='xyz',place_name='xyz'):

        number = self.related_space
        # self.entering_time=self.entering_time - timedelta(hours=5, minutes=41)
        # self.leaving_time=self.leaving_time - timedelta(hours=5, minutes=41)
        car_space_obj = CarTime.objects.filter(related_space=number,related_place=self.related_place)
        space_object_for_permission=Space.objects.select_for_update().get(space_number=number.space_number,related_place=self.related_place)
        print(space_object_for_permission.acess_to_space)

        if space_object_for_permission.acess_to_space==0:
            space_object_for_permission.acess_to_space+=1
            space_object_for_permission.save()
        else:
            return False


        if len(car_space_obj) > 0:
            for each in car_space_obj:
                correct_entering = each.entering_time
                correct_leaving = each.leaving_time
                # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                # correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                # correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)

                # restriction 5 minute ko
                correct_entering -= timedelta(minutes=5)
                correct_leaving += timedelta(minutes=5)
                # correct_entering = correct_entering.replace(tzinfo=pytz.timezone('UTC'))
                # correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('UTC'))

                # self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # print(type(correct_entering))

                # correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # print(type(self.entering_time))
                # print(self.entering_time)
                aune = (self.entering_time.replace(tzinfo=pytz.timezone('UTC')) + timedelta(minutes=0))
                jane = (self.leaving_time.replace(tzinfo=pytz.timezone('UTC')) + timedelta(minutes=0))
                # time delta ko object nikalna lai ho!not for arithmetic
                paila_aye_bhane = jane - correct_entering
                pachi_aye_bhane = aune - correct_leaving
                success = 'success'
                denied = 'denied'
                if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                    success = True
                    # print('first_if')
                    # if anonymous_person_name!='xyz':
                    #     print(place_name)
                    #
                    #     bike_obj=Bike.objects.create(user_name=User.objects.get(username=asociated_user),bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                    #     self.related_bike=bike_obj
                    # if anonymous_person_name=='xyz':
                    #     bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                    #                     place=self.related_place)
                    #     bike_obj.save()
                    #     self.related_bike = bike_obj
                    #
                    # self.save()
                    # space_obj = Space.objects.get(space_number=self.related_space)
                    # space_obj.empty = False
                    # space_obj.partial_occupied = True
                    # space_obj.save()
                    # return True
                elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                    success = True
                    # print(second_if)
                    # if anonymous_person_name!='xyz':
                    #     bike_obj=Bike.objects.create(user_name=User.objects.get(username=asociated_user),bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                    #     self.related_bike=bike_obj
                    # if anonymous_person_name=='xyz':
                    #     bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                    #                     place=self.related_place)
                    #     bike_obj.save()
                    #     self.related_bike = bike_obj
                    # self.save()
                    # space_obj = Space.objects.get(space_number=self.related_space)
                    # space_obj.empty = False
                    # space_obj.partial_occupied = True
                    # space_obj.save()
                    # return True
                    # print('you can save')
                else:
                    # print('i am wrong')
                    # return denied
                    space_object_for_permission.acess_to_space -= 1
                    space_object_for_permission.save()
                    return False
                    # if (b.total_seconds())>0:
                    print('yes,you,can inside1')
            if anonymous_person_name != 'xyz':

                car_obj = Car(user_name=User.objects.get(username=asociated_user),
                                               car_number=vehicle_number, place=Places.objects.get(name=place_name))
                car_objs = Car.objects.all()
                for car in car_objs:
                    if car.car_number == car_obj.car_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                car_obj.save()
                self.related_car = car_obj
            if anonymous_person_name == 'xyz':
                car_obj = Car(user_name=self.related_person, car_number=vehicle_number,
                                place=self.related_place)

                car_objs = Car.objects.all()
                for car in car_objs:
                    if car.car_number == car_obj.car_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False


                car_obj.save()



                self.related_car = car_obj

            self.save()




            space_obj = Space.objects.get(space_number=self.related_space,related_place=self.related_place)
            space_obj.empty = False
            space_obj.partial_occupied = True
            space_obj.save()
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return True
        else:
            success = 'success'
            # self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
            # self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
            if anonymous_person_name != 'xyz':
                car_obj = Car(user_name=User.objects.get(username=asociated_user),
                                               car_number=vehicle_number, place=Places.objects.get(name=place_name))
                car_objs = Car.objects.all()
                for car in car_objs:
                    if car.car_number == car_obj.car_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                car_obj.save()
                self.related_car = car_obj
            if anonymous_person_name == 'xyz':
                car_obj = Car(user_name=self.related_person, car_number=vehicle_number,
                                place=self.related_place)
                car_objs = Car.objects.all()
                for car in car_objs:
                    if car.car_number == car_obj.car_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                car_obj.save()

                # if space_object_for_permission.acess_to_space == 0:
                #     space_object_for_permission.acess_to_space -= 1
                #     space_object_for_permission.save()
                self.related_car = car_obj
            self.save()

            # if space_object_for_permission.acess_to_space == 0:
            #     space_object_for_permission.acess_to_space -= 1
            #     space_object_for_permission.save()

            # if space_object_for_permission.acess_to_space == 0:
            #     space_object_for_permission.acess_to_space -= 1
            #     space_object_for_permission.save()
            space_obj = Space.objects.get(space_number=self.related_space,related_place=Places.objects.get(name=place_name))
            space_obj.empty = False
            space_obj.partial_occupied = True
            space_obj.save()
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return True








    def payment(self):
        total_time=self.leaving_time-self.entering_time
        total_time_parked=total_time.total_seconds()/(60*60)
        total_time_parked=float(str(total_time_parked))
        print(datetime.now())
        print('present time')
        print(datetime.now())
        print('present time')
        extra_time_parked_in_minutes = 0
        if (self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))) < (
        datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu'))):
            print(self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu')))
            print(datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu')))
            extra_time = datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu')) - self.leaving_time.replace(
                tzinfo=pytz.timezone('Asia/Kathmandu'))
            extra_time_parked_in_minutes = extra_time.total_seconds() / 60
        list_of_time = [total_time_parked, extra_time_parked_in_minutes]
        return list_of_time
        # if self.leaving_time>datetime.now():
        #     extra_time=datetime.now()-self.leaving_time
        #     extra_time_parked_in_minutes=extra_time.total_seconds()/60
        # list_of_time=[total_time_parked,extra_time_parked_in_minutes]
        # return list_of_time
        # # return total_time_parked




















    def search_the_space(self):
        related_place = self.related_place
        # number=int(str(number))
        # car_space_obj=CarSpace.objects.filter(space_number=number)
        # car_space_obj = BikeTime.objects.filter(related_space=number)
        available_set = set()
        space_obj = Space.objects.filter(related_place=related_place)
        for obj in space_obj:
            if obj.car_space is True:
                time_obj = CarTime.objects.filter(related_space=obj)
                print('hi! i am trying hARD OK.')
                print(time_obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering)
                        print(correct_entering.tzinfo)
                        print("above this is entering")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=5)
                        correct_leaving += timedelta(minutes=5)

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering.tzinfo)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(type(correct_entering))

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))

                        aune = (self.entering_time + timedelta(minutes=0))
                        print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving

                        print(correct_entering)
                        print(self.leaving_time)
                        print('check mathi ko')
                        print(self.entering_time)
                        print(correct_leaving)
                        # b = correct_leaving - aune
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            print('you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('you can save')
                        else:
                            print('i am wrong')

                        # if (b.total_seconds())>0:
                        #   print('yes,you,can inside1')
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        return available_set




    def search_the_space_admin(self):
        # number = self.related_space
        # number=int(str(number))
        print("hi")
        print('hi')
        # car_space_obj=CarSpace.objects.filter(space_number=number)
        # car_space_obj = BikeTime.objects.filter(related_space=number)
        available_set = set()
        space_obj = Space.objects.filter(related_place=self.related_place)
        for obj in space_obj:
            if obj.car_space is True:
                time_obj = CarTime.objects.filter(related_space=obj)
                print('hi! i am trying hARD OK.')
                print(time_obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering)
                        print(correct_entering.tzinfo)
                        print("above this is entering")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=0)
                        correct_leaving += timedelta(minutes=0)

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering.tzinfo)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(type(correct_entering))

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))

                        aune = (self.entering_time + timedelta(minutes=0))
                        print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving

                        print(correct_entering)
                        print(self.leaving_time)
                        print('check mathi ko')
                        print(self.entering_time)
                        print(correct_leaving)
                        # b = correct_leaving - aune
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            print('you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('you can save')
                        else:
                            print('i am wrong')

                        # if (b.total_seconds())>0:
                        #   print('yes,you,can inside1')
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        return available_set













class BikeTime(models.Model):
    related_bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    related_person = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bitime')
    related_place = models.ForeignKey(Places, on_delete=models.CASCADE)
    related_space = models.ForeignKey(Space, on_delete=models.CASCADE,default=1)
    entering_time = models.DateTimeField()
    leaving_time = models.DateTimeField()

    def __str__(self):
        return str(self.related_space)

    @transaction.atomic
    def confirm_the_space(self,vehicle_number,place_name):
        related_place = self.related_place
        bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                        place=self.related_place)
        space_object_for_permission = Space.objects.select_for_update().get(
            space_number=self.related_space.space_number,
            related_place=self.related_place)

        if space_object_for_permission.acess_to_space == 0:
            space_object_for_permission.acess_to_space += 1
            space_object_for_permission.save()
        else:
            return False

        if len(BikeTime.objects.filter(related_space=self.related_space,related_place=Places.objects.get(name=place_name)))>0:
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return False
        else:
            # space_object_for_permission = Space.objects.select_for_update().get(
            #     space_number=self.related_space.space_number,
            #     related_place=self.related_place)
            bike_objs=Bike.objects.all()
            for bike in bike_objs:
                if bike.bike_number==bike_obj.bike_number:
                    space_object_for_permission.acess_to_space -= 1
                    space_object_for_permission.save()
                    return False

            bike_obj.save()
            self.related_bike=bike_obj

            self.save()

            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            space_obj=Space.objects.get(space_number=self.related_space,related_place=related_place)
            space_obj.empty = False
            space_obj.partial_occupied = True
            space_obj.save()
            return True

    def search_the_available_space(self):
        # a=0 #for test
        related_place = self.related_place
        available_set = set()
        space_obj = Space.objects.filter(related_place=related_place)
        # print(space_obj)
        for obj in space_obj:
            if obj.bike_space is True:
                time_obj = BikeTime.objects.filter(related_space=obj)
                # print(time_obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        print(correct_entering)
                        print(correct_leaving)
                        print("above this is entering time of database")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        # correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        # correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=5)
                        correct_leaving += timedelta(minutes=5)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('UTC'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('UTC'))
                        print(self.entering_time)
                        print(self.leaving_time)
                        aune = (self.entering_time + timedelta(minutes=0))
                        # print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        print(aune)
                        print(jane)
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            # a=a+1;
                            # print(a,'a')
                            print(jane)
                            print(aune)
                            print('first you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('second you can save')
                        else:
                            print('i am wrong')
                            break
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        print('availble sets',available_set)
        return available_set

    @transaction.atomic()
    def can_book(self,asociated_user='xyz',anonymous_person_name='xyz',vehicle_number='xyz',place_name='xyz'):
        number = self.related_space
        #self.entering_time=self.entering_time - timedelta(hours=5, minutes=41)
        #self.leaving_time=self.leaving_time - timedelta(hours=5, minutes=41)
        space_object_for_permission=Space.objects.select_for_update().get(space_number=number.space_number,related_place=self.related_place)
        if space_object_for_permission.acess_to_space==0:
            space_object_for_permission.acess_to_space+=1
            space_object_for_permission.save()
        else:
            return False

        bike_space_obj = BikeTime.objects.filter(related_space=number,related_place=self.related_place)
        if len(bike_space_obj) > 0:
            for each in bike_space_obj:
                correct_entering = each.entering_time
                correct_leaving = each.leaving_time

                # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                # correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                # correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)

                 # restriction 5 minute ko
                correct_entering -= timedelta(minutes=5)
                correct_leaving += timedelta(minutes=5)

                # correct_entering = correct_entering.replace(tzinfo=pytz.timezone('UTC'))
                # correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('UTC'))

                # self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # print(type(correct_entering))

                # correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                # correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                print(type(self.entering_time))
                print(self.entering_time)
                aune = (self.entering_time.replace(tzinfo=pytz.timezone('UTC')) + timedelta(minutes=0))
                jane = (self.leaving_time.replace(tzinfo=pytz.timezone('UTC')) + timedelta(minutes=0))
                # time delta ko object nikalna lai ho!not for arithmetic
                paila_aye_bhane = jane - correct_entering
                pachi_aye_bhane = aune - correct_leaving
                success = 'success'
                denied = 'denied'
                if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                    success=True
                    # print('first_if')
                    # if anonymous_person_name!='xyz':
                    #     print(place_name)
                    #
                    #     bike_obj=Bike.objects.create(user_name=User.objects.get(username=asociated_user),bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                    #     self.related_bike=bike_obj
                    # if anonymous_person_name=='xyz':
                    #     bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                    #                     place=self.related_place)
                    #     bike_obj.save()
                    #     self.related_bike = bike_obj
                    #
                    # self.save()
                    # space_obj = Space.objects.get(space_number=self.related_space)
                    # space_obj.empty = False
                    # space_obj.partial_occupied = True
                    # space_obj.save()
                    # return True
                elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                    success=True
                    # print(second_if)
                    # if anonymous_person_name!='xyz':
                    #     bike_obj=Bike.objects.create(user_name=User.objects.get(username=asociated_user),bike_number=vehicle_number,place=Places.objects.get(name=place_name))
                    #     self.related_bike=bike_obj
                    # if anonymous_person_name=='xyz':
                    #     bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                    #                     place=self.related_place)
                    #     bike_obj.save()
                    #     self.related_bike = bike_obj
                    # self.save()
                    # space_obj = Space.objects.get(space_number=self.related_space)
                    # space_obj.empty = False
                    # space_obj.partial_occupied = True
                    # space_obj.save()
                    # return True
                    #print('you can save')
                else:
                    #print('i am wrong')
                    space_object_for_permission.acess_to_space -= 1
                    space_object_for_permission.save()
                    #return denied
                    return False
                # if (b.total_seconds())>0:
                    print('yes,you,can inside1')
            if anonymous_person_name != 'xyz':

                bike_obj = Bike(user_name=User.objects.get(username=asociated_user),
                                               bike_number=vehicle_number, place=Places.objects.get(name=place_name))
                bike_objs = Bike.objects.all()
                for bike in bike_objs:
                    if bike.bike_number == bike_obj.bike_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                bike_obj.save()
                self.related_bike = bike_obj
            if anonymous_person_name == 'xyz':
                # if BikeTime.objects.get(entering_time=self.related_space.space_number).exists()

                bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                                place=self.related_place)
                bike_objs = Bike.objects.all()
                for bike in bike_objs:
                    if bike.bike_number == bike_obj.bike_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                bike_obj.save()
                self.related_bike = bike_obj

            self.save()
            space_obj = Space.objects.get(space_number=self.related_space,related_place=Places.objects.get(name=place_name))
            space_obj.empty = False
            space_obj.partial_occupied = True
            space_obj.save()
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return True
        else:
            success = 'success'
            # self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
            # self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
            if anonymous_person_name != 'xyz':
                bike_obj = Bike(user_name=User.objects.get(username=asociated_user),
                                               bike_number=vehicle_number, place=Places.objects.get(name=place_name))
                bike_objs = Bike.objects.all()
                for bike in bike_objs:
                    if bike.bike_number == bike_obj.bike_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False
                bike_obj.save()
                self.related_bike = bike_obj
            if anonymous_person_name == 'xyz':
                bike_obj = Bike(user_name=self.related_person, bike_number=vehicle_number,
                                place=self.related_place)
                bike_objs = Bike.objects.all()
                for bike in bike_objs:
                    if bike.bike_number == bike_obj.bike_number:
                        space_object_for_permission.acess_to_space -= 1
                        space_object_for_permission.save()
                        return False

                bike_obj.save()
                self.related_bike = bike_obj
            self.save()
            space_obj=Space.objects.get(space_number=self.related_space,related_place=Places.objects.get(name=place_name))
            space_obj.empty=False
            space_obj.partial_occupied=True
            space_obj.save()
            space_object_for_permission.acess_to_space -= 1
            space_object_for_permission.save()
            return True


    def payment(self):
        total_time = self.leaving_time - self.entering_time
        total_time_parked = total_time.total_seconds() / (60 * 60)
        # total_time_parked = float(str(total_time_parked))
        # return total_time_parked
        print(datetime.now())
        print('present time')
        extra_time_parked_in_minutes=0
        if (self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))) < (datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu'))):
            print(self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu')))
            print(datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu')))
            extra_time = datetime.now().replace(tzinfo=pytz.timezone('Asia/Kathmandu')) - self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
            extra_time_parked_in_minutes = extra_time.total_seconds() / 60
        list_of_time = [total_time_parked, extra_time_parked_in_minutes]
        return list_of_time

    def search_the_space(self):
        related_place = self.related_place
        # number=int(str(number))
        print("hi")
        print('hi')
        # car_space_obj=CarSpace.objects.filter(space_number=number)
        #car_space_obj = BikeTime.objects.filter(related_space=number)
        available_set=set()
        space_obj = Space.objects.filter(related_place=related_place)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print(space_obj)
        for obj in space_obj:

            if obj.bike_space is True:
                time_obj=BikeTime.objects.filter(related_space=obj)
                print('hi! i am trying hARD OK.')
                print(time_obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering)
                        print(correct_entering.tzinfo)
                        print("above this is entering")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=5)
                        correct_leaving += timedelta(minutes=5)

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering.tzinfo)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(type(correct_entering))

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))

                        aune = (self.entering_time + timedelta(minutes=0))
                        print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving

                        print(correct_entering)
                        print(self.leaving_time)
                        print('check mathi ko')
                        print(self.entering_time)
                        print(correct_leaving)
                        # b = correct_leaving - aune
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            print('you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('you can save')
                        else:
                            print('i am wrong')

                        # if (b.total_seconds())>0:
                        #   print('yes,you,can inside1')
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        return available_set


















    def search_the_space_admin(self):
        # number = self.related_space
        # number=int(str(number))
        print("hi")
        print('hi')
        # car_space_obj=CarSpace.objects.filter(space_number=number)
        # car_space_obj = BikeTime.objects.filter(related_space=number)
        available_set = set()
        space_obj = Space.objects.filter(related_place=self.related_place)
        for obj in space_obj:
            if obj.bike_space is True:
                time_obj = BikeTime.objects.filter(related_space=obj)
                print('hi! i am trying hARD OK.')
                print(time_obj)
                if len(time_obj) > 0:
                    for each in time_obj:
                        correct_entering = each.entering_time
                        correct_leaving = each.leaving_time
                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering)
                        print(correct_entering.tzinfo)
                        print("above this is entering")
                        # admin ko print garda extra 5:41 add garna parcha!ani balla user le enter garya time sahi auncha
                        correct_entering = each.entering_time + timedelta(hours=5, minutes=41)
                        correct_leaving = each.leaving_time + timedelta(hours=5, minutes=41)
                        # restriction 5 minute ko
                        correct_entering -= timedelta(minutes=0)
                        correct_leaving += timedelta(minutes=0)

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(correct_entering.tzinfo)
                        self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        print(type(correct_entering))

                        correct_entering = correct_entering.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                        correct_leaving = correct_leaving.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))

                        aune = (self.entering_time + timedelta(minutes=0))
                        print(aune.tzinfo)
                        print('aune ko lagi')
                        jane = (self.leaving_time + timedelta(minutes=0))
                        # time delta ko object nikalna lai ho!not for arithmetic
                        paila_aye_bhane = jane - correct_entering
                        pachi_aye_bhane = aune - correct_leaving

                        print(correct_entering)
                        print(self.leaving_time)
                        print('check mathi ko')
                        print(self.entering_time)
                        print(correct_leaving)
                        # b = correct_leaving - aune
                        print(paila_aye_bhane.total_seconds())
                        print(pachi_aye_bhane.total_seconds())
                        success = 'success'
                        denied = 'denied'
                        if (paila_aye_bhane.total_seconds()) > 0 and (pachi_aye_bhane.total_seconds()) > 0:
                            available_set.add(obj)
                            print('you can')
                        elif (paila_aye_bhane.total_seconds()) < 0 and (pachi_aye_bhane.total_seconds()) < 0:
                            available_set.add(obj)
                            print('you can save')
                        else:
                            print('i am wrong')

                        # if (b.total_seconds())>0:
                        #   print('yes,you,can inside1')
                else:
                    available_set.add(obj)
                    success = 'success'
                    self.entering_time = self.entering_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
                    self.leaving_time = self.leaving_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
        return available_set


