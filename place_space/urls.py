from django.urls import path
from .import views

app_name='place_space'

urlpatterns=[
    #path('place/<name>/<number>', views.tryy, name='space'),
    # path('place/<name>/', views.tryy, name='space'),
    # path('place_form/<name>/<space_number>/<truth>/',views.book_time,name='book_time'),
    # path('book/<name>/<space_number>/<entering_time>/<leaving_time>/<truth>/',views.book_click_time,name='book_click_time'),
    path('place/<name>/', views.show_the_space,name='space'),
    path('green_slots/<place_name>/',views.green_slots_entry,name='green_slots_entry'),
    path('booked_slots/<place_name>/',views.booked_slots_entry,name='booked_slots_entry'),
    path('search_the_space/<place_name>',views.search_the_space,name='search_the_space'),
    path('fetch_booked/<space_number>/<place_name>',views.fetch_booked,name='fetch_booked'),
    # path('proceeded_after_user_searched/<place_number>/<place_name>/<entering_time>/<leaving_time>/',views.proceeded_after_user_searched,name='proceeded_after_user_searched'),
    path('proceeded_after_user_searched/<place_name>/',views.proceeded_after_user_searched,name='proceeded_after_user_searched'),
    path('proceeded_after_user_searched/<place_number>/<place_name>/<entering_time>/<leaving_time>/<vehicle_type>/<vehicle_number>/<anonymous_person>/<phone_number>/',views.proceeded_after_user_searched,name='proceeded_after_user_searched')
]