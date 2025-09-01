from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'reservation_date', 'reservation_time', 'party_size', 'status', 'created_at')
    list_filter = ('status', 'reservation_date', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    ordering = ('-created_at',)
    list_editable = ('status',)
