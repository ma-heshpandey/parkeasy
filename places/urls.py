from django.urls import path,include
from .import views

app_name='places'

urlpatterns=[
    path('places/',views.place,name='place'),
    path('places/entry_of_place_by_admin',views.entry_of_place_by_admin,name='entry_of_place_by_admin'),
    path('view_maps/<name>',views.view_map,name='map'),
    path('full_maps/<name1>',views.only_map,name='only_map')
]