from django.contrib import admin
from django.urls import path,include
from .import views


app_name='admin_function'

urlpatterns = [
    path('<place_name>/', views.list_of_task, name='list_of_task'),
    path('payment/<place_name>/', views.payment, name='payment'),
    path('payment/<name>/<vehicle_number>/<space_number>/<place_name>/', views.display_payment, name='display_payment'),
    path('payment/<name>/<vehicle_number>/<space_number>/<place_name>/<booked_by>', views.display_payment, name='display_payment'),
    path('fetch_booked_to_show_for_admin/<space_number>/<place_name>',views.fetch_booked_to_show_for_admin,name='fetch_booked_to_show_for_admin'),
    path('delete_space_by_admin/<vehicle_number>/<space_number>/<place_name>',views.delete_space_by_admin,name='delete_space_by_admin'),
    path('manage_the_space/<vehicle_number>/<space_number>/<place_name>/<user_name>',views.manage_the_space,name='manage_the_space'),
]