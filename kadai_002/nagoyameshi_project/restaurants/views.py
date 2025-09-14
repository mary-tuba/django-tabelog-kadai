from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from accounts.decorators import premium_required
from .forms import RestaurantCreateForm
from .models import Restaurant, Favorite
from reviews.models import Review


def index(request):
    """店舗一覧ページ（トップページ）"""
    # 承認済みの店舗をランダムに5件取得
    restaurants = Restaurant.objects.filter(is_active=True).select_related('category').order_by('?')[:5]
    
    context = {
        'page_title': '店舗一覧',
        'restaurants': restaurants,
    }
    return render(request, 'restaurants/index.html', context)


def detail(request, restaurant_id):
    """店舗詳細ページ"""
    # 承認済みの店舗のみ表示
    restaurant = get_object_or_404(
        Restaurant.objects.select_related('category').filter(is_active=True), 
        id=restaurant_id
    )
    
    # プレミアムユーザーのみレビューを表示
    reviews = None
    user_review = None
    if request.user.is_authenticated and getattr(request.user, 'is_premium', False):
        # 公開されているレビューを取得
        reviews = Review.objects.filter(
            restaurant=restaurant,
            is_public=True
        ).select_related('user').order_by('-created_at')
        
        # ログインユーザーのレビューがあるかチェック
        user_review = Review.objects.filter(
            restaurant=restaurant,
            user=request.user
        ).first()
    
    # お気に入り状態をチェック（プレミアムユーザーのみ）
    user_favorite = False
    if request.user.is_authenticated and getattr(request.user, 'is_premium', False):
        user_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
    
    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'user_review': user_review,
        'user_favorite': user_favorite,
    }
    return render(request, 'restaurants/detail.html', context)


def search(request):
    """店舗検索ページ（ログイン不要）"""
    from categories.models import Category
    from django.db.models import Q
    
    # 検索パラメータを取得
    keyword = request.GET.get('keyword', '').strip()
    category_id = request.GET.get('category', '')
    budget_min = request.GET.get('budget_min', '')
    budget_max = request.GET.get('budget_max', '')
    sort_by = request.GET.get('sort', 'created_at')
    
    # 基本のクエリセット（承認済みの店舗のみ）
    restaurants = Restaurant.objects.filter(is_active=True).select_related('category')
    
    # キーワード検索（店舗名、説明、住所）
    if keyword:
        restaurants = restaurants.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(address__icontains=keyword)
        )
    
    # カテゴリ検索
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    
    # 予算検索
    try:
        if budget_min:
            restaurants = restaurants.filter(budget_max__gte=int(budget_min))
        if budget_max:
            restaurants = restaurants.filter(budget_min__lte=int(budget_max))
    except ValueError:
        pass
    
    # 並び替え
    if sort_by == 'name':
        restaurants = restaurants.order_by('name')
    elif sort_by == 'budget_min':
        restaurants = restaurants.order_by('budget_min')
    elif sort_by == 'budget_max':
        restaurants = restaurants.order_by('-budget_max')
    else:  # created_at
        restaurants = restaurants.order_by('-created_at')
    
    # ページネーション
    paginator = Paginator(restaurants, 9)  # 1ページ9件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # カテゴリ一覧を取得
    categories = Category.objects.all().order_by('name')
    
    context = {
        'page_title': '店舗検索',
        'categories': categories,
        'page_obj': page_obj,
        'keyword': keyword,
        'selected_category': category_id,
        'budget_min': budget_min,
        'budget_max': budget_max,
        'sort_by': sort_by,
        'result_count': restaurants.count(),
    }
    return render(request, 'restaurants/search.html', context)


@premium_required()
def create_restaurant(request):
    """店舗登録ページ（プレミアム会員限定）"""
    if request.method == 'POST':
        form = RestaurantCreateForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save()
            messages.success(
                request, 
                f'店舗「{restaurant.name}」の登録申請を受け付けました。'
                '管理者の承認後に公開されます。'
            )
            return redirect('restaurants:index')
        else:
            # フォームエラーがある場合
            messages.error(request, '入力内容に誤りがあります。下記をご確認ください。')
    else:
        form = RestaurantCreateForm()
    
    return render(request, 'restaurants/create.html', {'form': form})


@premium_required()
def my_restaurants(request):
    """自分が登録した店舗一覧（プレミアム会員限定）"""
    # 実装時はユーザーと店舗の関連付けが必要
    # 現在は仮実装
    restaurants = Restaurant.objects.filter(is_active=False)  # 承認待ちの店舗
    
    context = {
        'restaurants': restaurants,
        'page_title': '登録した店舗一覧'
    }
    return render(request, 'restaurants/my_restaurants.html', context)


@premium_required()
def add_favorite(request, restaurant_id):
    """お気に入りに追加"""
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
        
        try:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                restaurant=restaurant
            )
            
            if created:
                messages.success(request, f'「{restaurant.name}」をお気に入りに追加しました。')
                is_favorite = True
            else:
                messages.info(request, f'「{restaurant.name}」は既にお気に入りに登録済みです。')
                is_favorite = True
                
        except IntegrityError:
            messages.error(request, 'お気に入りの追加に失敗しました。')
            is_favorite = False
        
        # AJAX リクエストの場合は JSON で返す
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': created,
                'is_favorite': is_favorite,
                'message': messages.get_messages(request)._loaded_data[-1].message if messages.get_messages(request)._loaded_data else ''
            })
        
        return redirect('restaurants:detail', restaurant_id=restaurant_id)
    
    return redirect('restaurants:detail', restaurant_id=restaurant_id)


@premium_required()
def remove_favorite(request, restaurant_id):
    """お気に入りから削除"""
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        try:
            favorite = Favorite.objects.get(user=request.user, restaurant=restaurant)
            favorite.delete()
            messages.success(request, f'「{restaurant.name}」をお気に入りから削除しました。')
            is_favorite = False
            success = True
        except Favorite.DoesNotExist:
            messages.info(request, f'「{restaurant.name}」はお気に入りに登録されていません。')
            is_favorite = False
            success = False
        
        # AJAX リクエストの場合は JSON で返す
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'is_favorite': is_favorite,
                'message': messages.get_messages(request)._loaded_data[-1].message if messages.get_messages(request)._loaded_data else ''
            })
        
        return redirect('restaurants:detail', restaurant_id=restaurant_id)
    
    return redirect('restaurants:detail', restaurant_id=restaurant_id)


@premium_required()
def favorite_list(request):
    """お気に入り一覧"""
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant', 'restaurant__category').order_by('-created_at')
    
    # ページネーション
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'restaurants/favorite_list.html', context)
