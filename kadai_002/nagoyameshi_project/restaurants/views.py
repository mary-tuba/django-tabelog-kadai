from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.decorators import premium_required
from .forms import RestaurantCreateForm
from .models import Restaurant


def index(request):
    """店舗一覧ページ（トップページ）"""
    context = {
        'page_title': '店舗一覧',
        'restaurants': [
            {'id': 1, 'name': '味仙', 'category': '台湾料理', 'rating': 4.5},
            {'id': 2, 'name': '世界の山ちゃん', 'category': '手羽先', 'rating': 4.2},
            {'id': 3, 'name': 'コメダ珈琲店', 'category': '喫茶', 'rating': 4.0},
        ]
    }
    return render(request, 'restaurants/index.html', context)


def detail(request, restaurant_id):
    """店舗詳細ページ"""
    # ダミーデータ
    restaurant = {
        'id': restaurant_id,
        'name': '味仙',
        'category': '台湾料理',
        'rating': 4.5,
        'description': '名古屋名物の台湾料理店です。',
        'address': '愛知県名古屋市中区大須3-6-18',
        'phone': '052-241-5565',
        'opening_hours': '11:00-23:00',
    }
    
    context = {
        'restaurant': restaurant,
        'reviews': [
            {'user': 'user1', 'rating': 5, 'comment': '美味しかったです！'},
            {'user': 'user2', 'rating': 4, 'comment': '辛いけど癖になる味。'},
        ]
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
