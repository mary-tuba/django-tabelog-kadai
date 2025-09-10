from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from accounts.decorators import premium_required
from restaurants.models import Restaurant
from .models import Review
from .forms import ReviewCreateForm


@premium_required()
def create_review(request, restaurant_id):
    """レビュー作成（プレミアムユーザー限定）"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    
    # 既にレビュー済みかチェック
    existing_review = Review.objects.filter(user=request.user, restaurant=restaurant).first()
    if existing_review:
        messages.warning(request, 'この店舗には既にレビューを投稿されています。編集をご利用ください。')
        return redirect('restaurants:detail', restaurant_id=restaurant_id)
    
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.save()
                messages.success(request, f'「{restaurant.name}」へのレビューを投稿しました。')
                return redirect('restaurants:detail', restaurant_id=restaurant_id)
            except IntegrityError:
                messages.error(request, '既にこの店舗にレビューを投稿済みです。')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label if field != "__all__" else ""}: {error}')
    else:
        form = ReviewCreateForm()
    
    context = {
        'form': form,
        'restaurant': restaurant,
    }
    return render(request, 'reviews/create_review.html', context)


@premium_required()
def edit_review(request, review_id):
    """レビュー編集"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, f'「{review.restaurant.name}」へのレビューを更新しました。')
            return redirect('restaurants:detail', restaurant_id=review.restaurant.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label if field != "__all__" else ""}: {error}')
    else:
        form = ReviewCreateForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'restaurant': review.restaurant,
    }
    return render(request, 'reviews/edit_review.html', context)


@premium_required()
def delete_review(request, review_id):
    """レビュー削除"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        restaurant_id = review.restaurant.id
        restaurant_name = review.restaurant.name
        review.delete()
        messages.success(request, f'「{restaurant_name}」へのレビューを削除しました。')
        return redirect('restaurants:detail', restaurant_id=restaurant_id)
    
    context = {
        'review': review
    }
    return render(request, 'reviews/delete_review.html', context)


@premium_required()
def my_reviews(request):
    """マイレビュー一覧"""
    reviews = Review.objects.filter(user=request.user).select_related('restaurant', 'restaurant__category').order_by('-created_at')
    
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/my_reviews.html', context)