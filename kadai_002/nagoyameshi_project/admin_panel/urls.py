from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # ダッシュボード
    path('', views.dashboard, name='dashboard'),
    
    # 店舗管理
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/create/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/csv-import/', views.csv_import, name='csv_import'),
    path('restaurants/csv-sample/', views.csv_download_sample, name='csv_download_sample'),
    path('restaurants/csv-export/', views.restaurant_csv_export, name='restaurant_csv_export'),
    path('restaurants/<int:restaurant_id>/edit/', views.restaurant_edit, name='restaurant_edit'),
    path('restaurants/<int:restaurant_id>/approve/', views.restaurant_approve, name='restaurant_approve'),
    path('restaurants/<int:restaurant_id>/reject/', views.restaurant_reject, name='restaurant_reject'),
    path('restaurants/<int:restaurant_id>/delete/', views.restaurant_delete, name='restaurant_delete'),
    
    # 会員管理
    path('users/', views.user_list, name='user_list'),
    path('users/csv-export/', views.user_list_csv_export, name='user_list_csv_export'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:user_id>/password-reset/', views.user_password_reset, name='user_password_reset'),
    path('users/<int:user_id>/status-toggle/', views.user_status_toggle, name='user_status_toggle'),
    path('users/<int:user_id>/premium-toggle/', views.user_premium_toggle, name='user_premium_toggle'),
    
    # レビュー管理
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:review_id>/hide/', views.review_hide, name='review_hide'),
    path('reviews/<int:review_id>/show/', views.review_show, name='review_show'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    
    # 予約管理
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:reservation_id>/status-change/', views.reservation_status_change, name='reservation_status_change'),
    path('reservations/<int:reservation_id>/delete/', views.reservation_delete, name='reservation_delete'),
    
    # 売上管理
    path('sales/', views.sales_report, name='sales_report'),
    path('sales/daily/', views.sales_daily_report, name='sales_daily_report'),
    
    # 管理者管理機能
    path('admin-user/create/', views.admin_user_create, name='admin_user_create'),
    path('regular-user/create/', views.regular_user_create, name='regular_user_create'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('password-change/', views.admin_password_change, name='admin_password_change'),
    
    # 運営会社情報管理
    path('company-info/edit/', views.company_info_edit, name='company_info_edit'),
    
    # カテゴリ管理
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/csv-import/', views.category_csv_import, name='category_csv_import'),
    path('categories/csv-sample/', views.category_csv_download_sample, name='category_csv_download_sample'),
    path('categories/csv-export/', views.category_csv_export, name='category_csv_export'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
]