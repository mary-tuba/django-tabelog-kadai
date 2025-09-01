from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'is_public', 'created_at')
    list_filter = ('rating', 'is_public', 'created_at')
    search_fields = ('user__username', 'restaurant__name', 'comment')
    ordering = ('-created_at',)
    list_editable = ('is_public',)
