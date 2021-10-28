from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib.auth.views import LogoutView

app_name='user_detail'

urlpatterns = [
    #path('signup', views.sign_up, name='sign_up'),
    #path('gmail/<int:pk>', views.send_mails, name='gmails'),
    path('gmail/', views.send_mails, name='gmails'),
    path('signup/',views.UserSignUp.as_view(),name="sign_up"),
    path('update', views.update_user,name='update_user_info'),
    # path('signup/admin/',views.UserSignUpForAdmin.as_view(),name="sign_up_for_admin"),
    path('signup/admin/',views.sign_up_admin,name="sign_up_for_admin"),
    path('admin_register_confirmation/',views.admin_register_confirmation,name="admin_register_confirmation"),
    path('booking_detail_of_user/',views.booking_detail_of_user,name='booking_detail_of_user'),
    path('delete_space/<pk_key>', views.delete_space_bike, name='delete_space'),
    path('delete_space_car/<pk_key>', views.delete_space_car, name='delete_space_car'),
    path('change_the_vehicle_number/<place_name>/<vehicle_number>',views.change_the_vehicle_number,name='change_the_vehicle_number')

    # path('delete_user_details/',views.delete_user_details,name='delete_user_details')
]