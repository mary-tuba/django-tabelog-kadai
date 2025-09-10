from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # レビュー投稿
    path('create/<int:restaurant_id>/', views.create_review, name='create_review'),
    
    # レビュー編集・削除
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    
    # レビュー一覧
    path('my-reviews/', views.my_reviews, name='my_reviews'),
]