from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE = (
        ('client', 'Client voyageur'),
        ('agency', 'Agence de transport'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='client')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_set',
        blank=True,
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
