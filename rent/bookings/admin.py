from django.contrib import admin
from .models import Booking
 

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['renter', 'property', 'status', 'move_in_date', 'duration_months', 'created_at']
    list_filter = ['status', 'move_in_date']
    search_fields = ['renter__username', 'property__title']
    readonly_fields = ['created_at', 'updated_at']
