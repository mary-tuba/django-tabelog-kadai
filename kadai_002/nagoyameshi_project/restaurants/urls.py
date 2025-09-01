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
]