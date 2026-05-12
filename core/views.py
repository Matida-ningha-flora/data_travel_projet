from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from travels.models import Trip
from datetime import date

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    trips = Trip.objects.filter(departure_date__gte=date.today()).order_by('departure_date')[:6]
    return render(request, 'core/home.html', {'trips': trips})
