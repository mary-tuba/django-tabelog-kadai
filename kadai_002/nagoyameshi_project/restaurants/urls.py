from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    # トップページ（店舗一覧）
    path('', views.index, name='index'),
    
    # 店舗詳細
    path('<int:restaurant_id>/', views.detail, name='detail'),
    
    # 店舗検索
    path('search/', views.search, name='search'),
    
    # プレミアム会員限定機能
    path('create/', views.create_restaurant, name='create'),
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
]