from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, Booking
from datetime import date

def search_trips(request):
    trips = Trip.objects.filter(departure_date__gte=date.today())
    
    departure = request.GET.get('departure')
    if departure:
        trips = trips.filter(departure_city__icontains=departure)
    
    arrival = request.GET.get('arrival')
    if arrival:
        trips = trips.filter(arrival_city__icontains=arrival)
    
    travel_date = request.GET.get('date')
    if travel_date:
        trips = trips.filter(departure_date=travel_date)
    
    return render(request, 'travels/search_results.html', {'trips': trips})

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        
        if seats > trip.available_seats:
            messages.error(request, f'Il reste {trip.available_seats} places')
            return redirect('book_trip', trip_id=trip_id)
        
        booking = Booking.objects.create(
            user=request.user,
            trip=trip,
            seats_reserved=seats
        )
        trip.available_seats -= seats
        trip.save()
        
        messages.success(request, f'Réservation confirmée ! {seats} place(s)')
        return redirect('my_bookings')
    
    return render(request, 'travels/book_trip.html', {'trip': trip})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'travels/my_bookings.html', {'bookings': bookings})
