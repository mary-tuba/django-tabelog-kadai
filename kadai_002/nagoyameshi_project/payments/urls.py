from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Stripez
    path('subscribe/', views.subscribe, name='subscribe'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    
    # �ֹ��׷��
    path('subscription/', views.subscription_detail, name='subscription'),
    path('subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('subscription/update-card/', views.update_card, name='update_card'),
]