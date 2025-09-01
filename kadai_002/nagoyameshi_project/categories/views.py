from django.http import HttpResponse


def category_list(request):
    return HttpResponse('<h1>カテゴリ一覧</h1><p>工事中です</p>')

def restaurants_by_category(request, category_id):
    return HttpResponse(f'<h1>カテゴリ別店舗</h1><p>カテゴリID: {category_id}</p><p>工事中です</p>')