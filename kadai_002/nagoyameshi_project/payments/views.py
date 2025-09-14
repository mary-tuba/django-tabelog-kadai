from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import stripe
from .models import Subscription, PaymentHistory

# Stripe APIキーの設定
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def subscribe(request):
    """プレミアム会員登録ページ"""
    # 既にプレミアム会員の場合はリダイレクト
    if request.user.is_premium:
        messages.info(request, '既にプレミアム会員です。')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        try:
            # Stripeのチェックアウトセッションを作成
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                }],
                success_url=request.build_absolute_uri(reverse('payments:success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('payments:cancel')),
                customer_email=request.user.email,
                metadata={
                    'user_id': request.user.id,
                }
            )
            
            return redirect(checkout_session.url, code=303)
            
        except stripe.error.StripeError as e:
            messages.error(request, f'エラーが発生しました: {str(e)}')
            return redirect('payments:subscribe')
    
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'price': 300,  # 月額300円
    }
    return render(request, 'payments/subscribe.html', context)


@login_required
def payment_success(request):
    """決済成功ページ"""
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, '決済情報が見つかりません。')
        return redirect('accounts:profile')
    
    try:
        # Stripeセッションの取得
        session = stripe.checkout.Session.retrieve(session_id)
        
        # サブスクリプション情報の取得
        subscription = stripe.Subscription.retrieve(session.subscription)
        
        # データベースに保存
        sub, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'stripe_customer_id': session.customer,
                'stripe_subscription_id': session.subscription,
                'status': 'active',
                'current_period_start': timezone.datetime.fromtimestamp(subscription['current_period_start'], tz=timezone.utc) if 'current_period_start' in subscription else timezone.now(),
                'current_period_end': timezone.datetime.fromtimestamp(subscription['current_period_end'], tz=timezone.utc) if 'current_period_end' in subscription else timezone.now() + timedelta(days=30),
                'amount': 300,
            }
        )
        
        # ユーザーをプレミアム会員に更新
        request.user.is_premium = True
        request.user.save()
        
        # 決済履歴を記録
        PaymentHistory.objects.create(
            subscription=sub,
            stripe_payment_intent_id=session.payment_intent if hasattr(session, 'payment_intent') and session.payment_intent else '',
            amount=300,
            status='succeeded',
            payment_date=timezone.now()
        )
        
        messages.success(request, 'プレミアム会員への登録が完了しました！')
        return render(request, 'payments/payment_success.html', {'subscription': sub})
        
    except stripe.error.StripeError as e:
        messages.error(request, f'エラーが発生しました: {str(e)}')
        return redirect('accounts:profile')


@login_required
def payment_cancel(request):
    """決済キャンセルページ"""
    messages.info(request, '決済がキャンセルされました。')
    return render(request, 'payments/payment_cancel.html')


@login_required
def subscription_detail(request):
    """サブスクリプション詳細"""
    if not request.user.is_premium:
        messages.error(request, 'プレミアム会員ではありません。')
        return redirect('payments:subscribe')
    
    try:
        subscription = Subscription.objects.get(user=request.user)
        
        # Stripeから最新情報を取得
        payment_method = None
        if subscription.stripe_subscription_id:
            stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
            
            # 情報を更新
            subscription.status = stripe_sub['status'] if 'status' in stripe_sub else 'active'
            if 'current_period_end' in stripe_sub:
                subscription.current_period_end = timezone.datetime.fromtimestamp(
                    stripe_sub['current_period_end'], tz=timezone.utc
                )
            subscription.save()
            
            # カード情報を取得
            if subscription.stripe_customer_id:
                try:
                    # 顧客の支払い方法を取得
                    payment_methods = stripe.PaymentMethod.list(
                        customer=subscription.stripe_customer_id,
                        type='card'
                    )
                    if payment_methods.data:
                        payment_method = payment_methods.data[0]
                except stripe.error.StripeError:
                    pass
        
        # 決済履歴を取得
        payment_history = subscription.payment_history.all()[:10]
        
        context = {
            'subscription': subscription,
            'payment_history': payment_history,
            'payment_method': payment_method,
        }
        return render(request, 'payments/subscription_detail.html', context)
        
    except Subscription.DoesNotExist:
        messages.error(request, 'サブスクリプション情報が見つかりません。')
        return redirect('accounts:profile')


@login_required
def cancel_subscription(request):
    """サブスクリプション解約"""
    if not request.user.is_premium:
        messages.error(request, 'プレミアム会員ではありません。')
        return redirect('accounts:profile')
    
    try:
        subscription = Subscription.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Stripeでサブスクリプションをキャンセル
            if subscription.stripe_subscription_id:
                stripe_sub = stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=True
                )
                
                subscription.status = 'cancelled'
                subscription.save()
                
                messages.success(request, 
                    f'プレミアム会員の解約手続きが完了しました。'
                    f'{subscription.current_period_end.strftime("%Y年%m月%d日")}まではご利用いただけます。'
                )
            
            return redirect('payments:subscription')
        
        context = {
            'subscription': subscription,
        }
        return render(request, 'payments/cancel_subscription.html', context)
        
    except Subscription.DoesNotExist:
        messages.error(request, 'サブスクリプション情報が見つかりません。')
        return redirect('accounts:profile')


@login_required
def update_card(request):
    """カード情報更新"""
    if not request.user.is_premium:
        messages.error(request, "プレミアム会員ではありません。")
        return redirect("payments:subscribe")
    
    if request.method == "POST":
        payment_method_id = request.POST.get("payment_method_id")
        
        if not payment_method_id:
            messages.error(request, "カード情報が正しく送信されませんでした。")
            return redirect("payments:subscription")
        
        try:
            subscription = Subscription.objects.get(user=request.user)
            
            if subscription.stripe_customer_id:
                # 既存の支払い方法を新しいものに置き換え
                payment_method = stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=subscription.stripe_customer_id,
                )
                
                # デフォルトの支払い方法として設定
                stripe.Customer.modify(
                    subscription.stripe_customer_id,
                    invoice_settings={
                        "default_payment_method": payment_method_id,
                    },
                )
                
                # サブスクリプションの支払い方法も更新
                if subscription.stripe_subscription_id:
                    stripe.Subscription.modify(
                        subscription.stripe_subscription_id,
                        default_payment_method=payment_method_id,
                    )
                
                messages.success(request, "カード情報を更新しました。")
            else:
                messages.error(request, "顧客情報が見つかりません。")
                
        except stripe.error.StripeError as e:
            messages.error(request, f"カード情報の更新に失敗しました: {str(e)}")
        except Subscription.DoesNotExist:
            messages.error(request, "サブスクリプション情報が見つかりません。")
    
    return redirect("payments:subscription")
