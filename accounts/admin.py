from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'phone', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Infos supplémentaires', {'fields': ('user_type', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Infos supplémentaires', {'fields': ('user_type', 'phone', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)
