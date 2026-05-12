from django.db import models
from django.conf import settings

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField(default=50)
    agency = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'agency'})
    
    def __str__(self):
        return f"{self.bus_number} ({self.capacity} places)"

class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.available_seats:
            self.available_seats = self.bus.capacity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.departure_city} → {self.arrival_city} ({self.departure_date})"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seats_reserved = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='confirmed')
    
    def __str__(self):
        return f"{self.user.username} - {self.trip}"
