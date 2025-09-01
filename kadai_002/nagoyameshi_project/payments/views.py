from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def subscribe(request):
    return HttpResponse('<h1>プレミアム会員登録</h1><p>工事中です</p>')

@login_required
def payment_success(request):
    return HttpResponse('<h1>決済完了</h1><p>工事中です</p>')

@login_required
def payment_cancel(request):
    return HttpResponse('<h1>決済キャンセル</h1><p>工事中です</p>')

@login_required
def subscription_detail(request):
    return HttpResponse('<h1>サブスクリプション詳細</h1><p>工事中です</p>')

@login_required
def cancel_subscription(request):
    return HttpResponse('<h1>サブスクリプション解約</h1><p>工事中です</p>')