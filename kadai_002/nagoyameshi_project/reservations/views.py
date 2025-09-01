from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def create_reservation(request, restaurant_id):
    return HttpResponse(f'<h1>予約作成</h1><p>店舗ID: {restaurant_id}</p><p>工事中です</p>')

@login_required
def reservation_list(request):
    return HttpResponse('<h1>予約一覧</h1><p>工事中です</p>')

@login_required
def reservation_detail(request, reservation_id):
    return HttpResponse(f'<h1>予約詳細</h1><p>予約ID: {reservation_id}</p><p>工事中です</p>')

@login_required
def cancel_reservation(request, reservation_id):
    return HttpResponse(f'<h1>予約キャンセル</h1><p>予約ID: {reservation_id}</p><p>工事中です</p>')