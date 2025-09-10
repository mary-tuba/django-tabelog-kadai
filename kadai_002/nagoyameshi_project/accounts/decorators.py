from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from functools import wraps


def premium_required(redirect_url=None, message=None):
    """
    プレミアム会員のみがアクセス可能なビューのデコレーター
    
    Args:
        redirect_url: プレミアム会員でない場合のリダイレクト先（デフォルト: premium_upgrade）
        message: プレミアム会員でない場合のメッセージ
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # まずログインが必要
        def wrapper(request, *args, **kwargs):
            # プレミアム会員チェック
            if hasattr(request.user, 'is_premium') and request.user.is_premium:
                return view_func(request, *args, **kwargs)
            
            # プレミアム会員でない場合
            default_message = (
                'この機能はプレミアム会員限定です。'
                'プレミアム会員になって、より多くの機能をご利用ください。'
            )
            messages.warning(request, message or default_message)
            
            # リダイレクト先の決定
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect('accounts:premium_upgrade')
        
        return wrapper
    return decorator


def premium_or_staff_required(redirect_url=None, message=None):
    """
    プレミアム会員またはスタッフのみがアクセス可能なビューのデコレーター
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # プレミアム会員またはスタッフチェック
            is_premium = hasattr(request.user, 'is_premium') and request.user.is_premium
            if is_premium or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            # 条件を満たさない場合
            default_message = (
                'この機能はプレミアム会員限定です。'
                'プレミアム会員になって、より多くの機能をご利用ください。'
            )
            messages.warning(request, message or default_message)
            
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect('accounts:premium_upgrade')
        
        return wrapper
    return decorator