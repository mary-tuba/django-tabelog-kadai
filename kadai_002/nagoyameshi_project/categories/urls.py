from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # カテゴリ一覧
    path('', views.category_list, name='list'),
    
    # カテゴリ別店舗一覧
    path('<int:category_id>/', views.restaurants_by_category, name='restaurants'),
]