from django.urls import path,include
from . import views

app_name='vehicle_info'

urlpatterns=[
    path('car_register/<name>',views.car_register,name='car_register'),
    path('bike_register/<name>',views.bike_register,name='bike_register'),
    #path('check_in/<name>/',views.vehicle_status,name='vehicle_status'),
    path('check_in/<number>/',views.check_in,name='check_in'),

]