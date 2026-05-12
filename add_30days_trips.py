import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dada_travel.settings')
django.setup()

from accounts.models import User
from travels.models import Bus, Trip

print("🚌 Ajout de trajets sur 30 jours...")

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
bus5, _ = Bus.objects.get_or_create(bus_number='REG-005', defaults={'capacity': 35, 'agency': agency})
print("✓ 5 bus créés")

# Toutes les villes du Cameroun
cities = {
    'Douala': 5000,
    'Yaoundé': 5000,
    'Bafoussam': 4500,
    'Garoua': 12000,
    'Maroua': 15000,
    'Kribi': 3500,
    'Limbe': 3000,
    'Ngaoundéré': 10000,
    'Bertoua': 7000,
    'Ebolowa': 4000,
    'Bamenda': 8000,
    'Foumban': 6000,
    'Dschang': 5500,
    'Buea': 3500,
    'Edéa': 2500,
    'Mbouda': 5000,
    'Kumba': 4000,
    'Mbalmayo': 3500,
    'Mokolo': 14000,
    'Bafang': 4800
}

# Destinations principales populaires
popular_routes = [
    ('Douala', 'Yaoundé', 5000, [6, 8, 10, 13, 15, 17, 19, 21]),
    ('Douala', 'Bafoussam', 4500, [7, 9, 11, 14, 16, 18]),
    ('Douala', 'Garoua', 12000, [5, 6, 8, 9]),
    ('Douala', 'Kribi', 3500, [7, 9, 11, 14, 17]),
    ('Douala', 'Limbe', 3000, [8, 10, 12, 14, 16, 18]),
    ('Douala', 'Bamenda', 8000, [6, 8, 10, 12, 14]),
    ('Douala', 'Buea', 3500, [7, 10, 13, 16]),
    ('Douala', 'Edéa', 2500, [6, 9, 12, 15, 18]),
    
    ('Yaoundé', 'Douala', 5000, [6, 8, 10, 13, 15, 17, 19]),
    ('Yaoundé', 'Bafoussam', 4500, [7, 9, 11, 13, 15]),
    ('Yaoundé', 'Kribi', 4000, [8, 11, 14]),
    ('Yaoundé', 'Bertoua', 5000, [8, 11, 14, 16]),
    ('Yaoundé', 'Ebolowa', 3500, [8, 10, 13, 16]),
    ('Yaoundé', 'Mbalmayo', 2500, [7, 10, 13, 16, 18]),
    
    ('Bafoussam', 'Douala', 4500, [6, 8, 10, 12, 14, 16, 18]),
    ('Bafoussam', 'Yaoundé', 4500, [7, 9, 11, 14]),
    ('Bafoussam', 'Dschang', 2500, [8, 11, 14, 17]),
    ('Bafoussam', 'Foumban', 4000, [7, 10, 13]),
    
    ('Kribi', 'Douala', 3500, [6, 9, 12, 15, 17]),
    ('Kribi', 'Yaoundé', 4000, [7, 10, 13, 16]),
    ('Kribi', 'Edéa', 2000, [8, 11, 14]),
    
    ('Garoua', 'Douala', 12000, [5, 7, 9]),
    ('Garoua', 'Maroua', 5000, [6, 9, 12]),
    ('Garoua', 'Ngaoundéré', 6000, [7, 10, 13]),
    
    ('Maroua', 'Douala', 15000, [6, 8]),
    ('Maroua', 'Garoua', 5000, [7, 10, 13]),
    ('Maroua', 'Mokolo', 3000, [8, 11, 14]),
    
    ('Bamenda', 'Douala', 8000, [6, 9, 12, 15]),
    ('Bamenda', 'Bafoussam', 3500, [7, 10, 13, 16]),
    ('Bamenda', 'Mbouda', 2000, [8, 11, 14]),
]

# Assigner les bus en alternance
buses = [bus1, bus2, bus3, bus4, bus5] * 20

# Date de départ sur 30 jours
start_date = date.today()
days = 30

count = 0
skipped = 0

for idx, (dep, arr, price, hours) in enumerate(popular_routes):
    bus = buses[idx % len(buses)]
    for day in range(days):
        trip_date = start_date + timedelta(days=day + 1)
        for hour in hours:
            trip_time = time(hour, 0)
            
            # Vérifier si le trajet existe déjà
            existing = Trip.objects.filter(
                bus=bus,
                departure_city=dep,
                arrival_city=arr,
                departure_date=trip_date,
                departure_time=trip_time
            ).first()
            
            if not existing:
                Trip.objects.create(
                    bus=bus,
                    departure_city=dep,
                    arrival_city=arr,
                    departure_date=trip_date,
                    departure_time=trip_time,
                    price=price,
                    available_seats=bus.capacity
                )
                count += 1
            else:
                skipped += 1

print(f"\n✅ {count} nouveaux trajets ajoutés !")
print(f"⏭️ {skipped} trajets déjà existants ignorés")
print(f"📊 Total trajets disponibles : {Trip.objects.count()}")

# Afficher le résumé par destination
print("\n📋 Résumé des trajets :")
from django.db.models import Count
summary = Trip.objects.values('departure_city', 'arrival_city').annotate(total=Count('id')).order_by('-total')[:15]
for s in summary:
    print(f"   • {s['departure_city']} → {s['arrival_city']} : {s['total']} trajets")

# Afficher les prochains jours
print(f"\n📅 Trajets par date :")
from collections import Counter
dates = Trip.objects.values_list('departure_date', flat=True)
date_counts = Counter(dates)
for d in sorted(date_counts.keys())[:15]:
    print(f"   • {d} : {date_counts[d]} départs")

print("\n✅ Terminé !")
