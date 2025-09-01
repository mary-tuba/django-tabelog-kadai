from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # ダッシュボード
    path('', views.dashboard, name='dashboard'),
    
    # 店舗管理
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/create/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/<int:restaurant_id>/edit/', views.restaurant_edit, name='restaurant_edit'),
    path('restaurants/<int:restaurant_id>/delete/', views.restaurant_delete, name='restaurant_delete'),
    
    # 会員管理
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # レビュー管理
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:review_id>/hide/', views.review_hide, name='review_hide'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    
    # 売上管理
    path('sales/', views.sales_report, name='sales_report'),
]