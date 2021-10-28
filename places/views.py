from django.shortcuts import render
from .models import Places
from place_space.models import Space

from .forms import  PlacesFormToRegister
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

@login_required(login_url='/login/')
def place(request):
    place_list=Places.objects.all()
    place_list_to_send=[]
    for place in place_list:
        if place.associate_admin.is_active is True:
            place_list_to_send.append(place)
        else:
            pass
    print(place_list)

    # place_list=list(place_list)
    return render(request,'places/places_list.html', {'place_list': place_list_to_send})



def entry_of_place_by_admin(request):
    if request.method == 'POST':
        form = PlacesFormToRegister(request.POST)
        if form.is_valid():
            place_name=form.cleaned_data['name']
            location=form.cleaned_data['location']
            number_of_car_space=form.cleaned_data['number_of_car_space']
            number_of_bike_space=form.cleaned_data['number_of_bike_space']
            place_link=form.cleaned_data['place_link']
            place_obj=Places(associate_admin=request.user,place_link=place_link,name=place_name,location=location,number_of_bike_space=number_of_bike_space,number_of_car_space=number_of_car_space)
            place_obj.save()
            for i in range(number_of_car_space):
                space_obj=Space(car_space=True,related_place=place_obj,space_number=f'C{i+1}')
                space_obj.save()

            for i in range(number_of_bike_space):
                space_obj=Space(bike_space=True,related_place=place_obj,space_number=f'B{i+1}')
                space_obj.save()

            request.user.is_active = False
            request.user.save()
            # return redirect('park:gmails',username=name)
            # return redirect('user_detail:gmails')
            return redirect('user_detail:admin_register_confirmation')

            return redirect('places:place')

    else:
        form = PlacesFormToRegister()
    return render(request, 'places/entry_form_of_place_for_admin.html', {'form': form})


@login_required(login_url='/login/')
def view_map(request,name):
    mapbox_access_token='pk.eyJ1IjoibWFoZXNoMjY4IiwiYSI6ImNrYTlhY3lqNDA1Y2IyeHA3cDdwajNoMW0ifQ.HPMCXdamzRiX9lwvLA-5LQ';
    return render(request,'places/map_of_place.html',{'mapbox_access_token': mapbox_access_token,'name':name })

@login_required(login_url='/login/')
def only_map(request,name1):
    return render(request,'places/full_default_map.html',{'name':name1})
