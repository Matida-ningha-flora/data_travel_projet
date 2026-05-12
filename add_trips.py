import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dada_travel.settings')
django.setup()

from accounts.models import User
from travels.models import Bus, Trip

# Récupérer ou créer une agence
agency, created = User.objects.get_or_create(
    username='agence_officielle',
    defaults={'user_type': 'agency'}
)
if created:
    agency.set_password('agence123')
    agency.save()
    print("✓ Agence créée")

# Créer des bus
bus1, _ = Bus.objects.get_or_create(bus_number='DAD-001', defaults={'capacity': 50, 'agency': agency})
bus2, _ = Bus.objects.get_or_create(bus_number='DAD-002', defaults={'capacity': 45, 'agency': agency})
bus3, _ = Bus.objects.get_or_create(bus_number='VIP-003', defaults={'capacity': 30, 'agency': agency})
bus4, _ = Bus.objects.get_or_create(bus_number='EXP-004', defaults={'capacity': 40, 'agency': agency})
print("✓ Bus créés")

# Supprimer les anciens trajets (optionnel - décommente si besoin)
# Trip.objects.all().delete()
# print("✓ Anciens trajets supprimés")

# Destinations populaires
destinations = [
    ('Douala', 'Yaoundé', 5000, [6, 8, 10, 13, 15, 17]),
    ('Douala', 'Bafoussam', 4500, [7, 9, 12, 14, 16]),
    ('Douala', 'Garoua', 12000, [5, 8]),
    ('Douala', 'Maroua', 15000, [6, 9]),
    ('Douala', 'Kribi', 3500, [8, 11, 14, 17]),
    ('Douala', 'Limbe', 3000, [7, 10, 13, 16]),
    ('Douala', 'Ngaoundéré', 10000, [7, 10]),
    ('Douala', 'Bertoua', 7000, [8, 11, 14]),
    ('Douala', 'Ebolowa', 4000, [9, 12, 15]),
    ('Douala', 'Bamenda', 8000, [6, 9, 12]),
    
    ('Yaoundé', 'Douala', 5000, [6, 8, 10, 13, 15, 17]),
    ('Yaoundé', 'Bafoussam', 4500, [7, 9, 12]),
    ('Yaoundé', 'Kribi', 4000, [8, 11, 14]),
    ('Yaoundé', 'Bertoua', 5000, [9, 12, 15]),
    ('Yaoundé', 'Ebolowa', 3500, [8, 11, 14]),
    
    ('Bafoussam', 'Douala', 4500, [6, 8, 10, 12, 14, 16]),
    ('Bafoussam', 'Yaoundé', 4500, [7, 9, 11, 13]),
    
    ('Garoua', 'Douala', 12000, [6, 9]),
    ('Maroua', 'Douala', 15000, [7, 10]),
    
    ('Kribi', 'Douala', 3500, [6, 9, 12, 15]),
    ('Kribi', 'Yaoundé', 4000, [7, 10, 13]),
]

# Associer les bus
buses = [bus1, bus2, bus3, bus4, bus1, bus2, bus3, bus1, bus2, bus3,
         bus4, bus1, bus2, bus3, bus1, bus2, bus3, bus4, bus1, bus2, bus3]

# Dates sur 21 jours
start_date = date.today()
days = 21

count = 0
for idx, (dep, arr, price, hours) in enumerate(destinations):
    bus = buses[idx % len(buses)]
    for day in range(days):
        trip_date = start_date + timedelta(days=day+1)
        for hour in hours:
            trip_time = time(hour, 0)
            trip, created = Trip.objects.get_or_create(
                bus=bus,
                departure_city=dep,
                arrival_city=arr,
                departure_date=trip_date,
                departure_time=trip_time,
                defaults={'price': price, 'available_seats': bus.capacity}
            )
            if created:
                count += 1

print(f"\n✅ {count} trajets ajoutés !")
print(f"📊 Total : {Trip.objects.count()} trajets disponibles")

# Résumé par destination
print("\n📋 Résumé par destination :")
from django.db.models import Count
summary = Trip.objects.values('departure_city', 'arrival_city').annotate(total=Count('id')).order_by('departure_city')
for s in summary:
    print(f"   • {s['departure_city']} → {s['arrival_city']} : {s['total']} trajets")
