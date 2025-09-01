from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # �\
    path('create/<int:restaurant_id>/', views.create_reservation, name='create'),
    
    # ��
    path('', views.reservation_list, name='list'),
    path('<int:reservation_id>/', views.reservation_detail, name='detail'),
    path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel'),
]