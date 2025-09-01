from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def dashboard(request):
    return HttpResponse('<h1>管理者ダッシュボード</h1><p>工事中です</p>')

@staff_member_required
def restaurant_list(request):
    return HttpResponse('<h1>店舗管理</h1><p>工事中です</p>')

@staff_member_required
def restaurant_create(request):
    return HttpResponse('<h1>店舗登録</h1><p>工事中です</p>')

@staff_member_required
def restaurant_edit(request, restaurant_id):
    return HttpResponse(f'<h1>店舗編集</h1><p>店舗ID: {restaurant_id}</p><p>工事中です</p>')

@staff_member_required
def restaurant_delete(request, restaurant_id):
    return HttpResponse(f'<h1>店舗削除</h1><p>店舗ID: {restaurant_id}</p><p>工事中です</p>')

@staff_member_required
def user_list(request):
    return HttpResponse('<h1>会員管理</h1><p>工事中です</p>')

@staff_member_required
def user_detail(request, user_id):
    return HttpResponse(f'<h1>会員詳細</h1><p>会員ID: {user_id}</p><p>工事中です</p>')

@staff_member_required
def user_delete(request, user_id):
    return HttpResponse(f'<h1>会員削除</h1><p>会員ID: {user_id}</p><p>工事中です</p>')

@staff_member_required
def review_list(request):
    return HttpResponse('<h1>レビュー管理</h1><p>工事中です</p>')

@staff_member_required
def review_hide(request, review_id):
    return HttpResponse(f'<h1>レビュー非公開</h1><p>レビューID: {review_id}</p><p>工事中です</p>')

@staff_member_required
def review_delete(request, review_id):
    return HttpResponse(f'<h1>レビュー削除</h1><p>レビューID: {review_id}</p><p>工事中です</p>')

@staff_member_required
def sales_report(request):
    return HttpResponse('<h1>売上管理</h1><p>工事中です</p>')