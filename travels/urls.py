from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_trips, name='search_trips'),
    path('book/<int:trip_id>/', views.book_trip, name='book_trip'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
