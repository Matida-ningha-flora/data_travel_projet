from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parcel, ParcelTracking

@login_required
def send_parcel(request):
    if request.method == 'POST':
        try:
            # Récupérer les données
            weight_str = request.POST.get('weight', '0').replace(',', '.')
            price_str = request.POST.get('price', '0').replace(',', '.')
            
            # Créer le colis
            parcel = Parcel(
                sender=request.user,
                receiver_name=request.POST.get('receiver_name'),
                receiver_phone=request.POST.get('receiver_phone'),
                receiver_address=request.POST.get('receiver_address'),
                departure_city=request.POST.get('departure_city'),
                arrival_city=request.POST.get('arrival_city'),
                weight=float(weight_str),
                description=request.POST.get('description', ''),
                price=float(price_str),
            )
            parcel.save()
            
            # Ajouter le premier suivi
            ParcelTracking.objects.create(
                parcel=parcel,
                location=parcel.departure_city,
                status='Enregistré',
                description=f'Colis enregistré par {request.user.username}'
            )
            
            messages.success(request, f'✅ Colis créé ! Numéro de suivi: {parcel.tracking_number}')
            return redirect('track_parcel', tracking_number=parcel.tracking_number)
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('send_parcel')
    
    return render(request, 'parcels/send_parcel.html')

@login_required
def track_parcel(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    return render(request, 'parcels/track_parcel.html', {'parcel': parcel})

@login_required
def my_parcels(request):
    parcels = Parcel.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'parcels/my_parcels.html', {'parcels': parcels})
