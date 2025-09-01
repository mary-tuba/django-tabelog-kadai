from django.contrib import admin
from .models import Restaurant, Favorite


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'budget_min', 'budget_max', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'address')
    ordering = ('-created_at',)
    list_editable = ('is_active',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'restaurant__name')
    ordering = ('-created_at',)
