from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from accounts.decorators import premium_required
from .forms import RestaurantCreateForm
from .models import Restaurant


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
    
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurants/detail.html', context)


def search(request):
    """店舗検索ページ"""
    context = {
        'page_title': '店舗検索',
        'categories': ['台湾料理', '手羽先', '喫茶', 'ひつまぶし', '味噌カツ']
    }
    return render(request, 'restaurants/search.html', context)


@premium_required()
def create_restaurant(request):
    """店舗登録ページ（プレミアム会員限定）"""
    if request.method == 'POST':
        form = RestaurantCreateForm(request.POST)
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
