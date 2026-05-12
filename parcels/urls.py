from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_parcel, name='send_parcel'),
    path('track/<str:tracking_number>/', views.track_parcel, name='track_parcel'),
    path('my-parcels/', views.my_parcels, name='my_parcels'),
]
