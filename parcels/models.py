from django.db import models
from django.conf import settings
import random

class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('picked_up', 'Récupéré'),
        ('in_transit', 'En transit'),
        ('delivered', 'Livré'),
    ]
    
    tracking_number = models.CharField(max_length=50, unique=True, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_parcels')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_address = models.TextField()
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            # Générer un numéro unique
            while True:
                new_tracking = f"DAD{random.randint(100000, 999999)}{random.randint(10, 99)}"
                if not Parcel.objects.filter(tracking_number=new_tracking).exists():
                    self.tracking_number = new_tracking
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tracking_number} - {self.sender.username}"

class ParcelTracking(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='trackings')
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.parcel.tracking_number} - {self.status}"
