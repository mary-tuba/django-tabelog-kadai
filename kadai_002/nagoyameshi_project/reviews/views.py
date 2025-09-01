from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def create_review(request, restaurant_id):
    return HttpResponse(f'<h1>レビュー投稿</h1><p>店舗ID: {restaurant_id}</p><p>工事中です</p>')

@login_required
def edit_review(request, review_id):
    return HttpResponse(f'<h1>レビュー編集</h1><p>レビューID: {review_id}</p><p>工事中です</p>')

@login_required
def delete_review(request, review_id):
    return HttpResponse(f'<h1>レビュー削除</h1><p>レビューID: {review_id}</p><p>工事中です</p>')

@login_required
def my_reviews(request):
    return HttpResponse('<h1>マイレビュー</h1><p>工事中です</p>')