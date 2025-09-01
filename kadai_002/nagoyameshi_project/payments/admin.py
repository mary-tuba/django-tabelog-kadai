from django.contrib import admin
from .models import Subscription, PaymentHistory


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'current_period_start', 'current_period_end', 'amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'stripe_customer_id')
    ordering = ('-created_at',)
    list_editable = ('status',)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'status', 'payment_date', 'created_at')
    list_filter = ('status', 'payment_date', 'created_at')
    search_fields = ('subscription__user__username', 'stripe_payment_intent_id')
    ordering = ('-created_at',)
