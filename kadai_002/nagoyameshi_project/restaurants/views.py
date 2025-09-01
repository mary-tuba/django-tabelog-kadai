from django.shortcuts import render
from django.http import HttpResponse


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
