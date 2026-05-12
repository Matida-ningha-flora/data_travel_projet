from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('travels/', include('travels.urls')),
    path('parcels/', include('parcels.urls')),
    path('booking/', include('booking.urls')),
]
