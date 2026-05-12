import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dada_travel.settings')
django.setup()

from accounts.models import User

# Créer une agence
agency, created = User.objects.get_or_create(
    username='agence_dakar',
    defaults={
        'password': 'agence123',
        'email': 'agence@dadatravel.com',
        'user_type': 'agency',
        'phone': '771234567',
        'address': 'Dakar, Sénégal'
    }
)

if created:
    agency.set_password('agence123')
    agency.save()
    print(f"✓ Agence créée : {agency.username} - {agency.user_type}")
else:
    print(f"✓ Agence existe déjà : {agency.username}")

# Créer un client
client, created = User.objects.get_or_create(
    username='client_test',
    defaults={
        'password': 'client123',
        'email': 'client@test.com',
        'user_type': 'client',
        'phone': '778899001',
        'address': 'Dakar'
    }
)

if created:
    client.set_password('client123')
    client.save()
    print(f"✓ Client créé : {client.username} - {client.user_type}")
else:
    print(f"✓ Client existe déjà : {client.username}")

print("\nListe des utilisateurs :")
for user in User.objects.all():
    print(f"  - {user.username} ({user.user_type})")
