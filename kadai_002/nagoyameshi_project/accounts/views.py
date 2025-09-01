from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse


def login_view(request):
    """ログインページ"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'ログインしました。')
            return redirect('restaurants:index')
        else:
            messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """ログアウト"""
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('restaurants:index')


def signup_view(request):
    """会員登録ページ"""
    if request.method == 'POST':
        messages.info(request, '会員登録機能は実装中です。')
    
    return render(request, 'accounts/signup.html')


@login_required
def profile_view(request):
    """プロフィール表示ページ"""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit_view(request):
    """プロフィール編集ページ"""
    if request.method == 'POST':
        messages.info(request, 'プロフィール編集機能は実装中です。')
    
    return render(request, 'accounts/profile_edit.html')


@login_required
def password_change_view(request):
    """パスワード変更ページ"""
    if request.method == 'POST':
        messages.info(request, 'パスワード変更機能は実装中です。')
    
    return render(request, 'accounts/password_change.html')


@login_required
def premium_upgrade_view(request):
    """プレミアム会員アップグレードページ"""
    if request.method == 'POST':
        messages.info(request, 'プレミアム会員機能は実装中です。')
    
    return render(request, 'accounts/premium_upgrade.html')


@login_required
def premium_cancel_view(request):
    """プレミアム会員解約ページ"""
    if request.method == 'POST':
        messages.info(request, 'プレミアム会員解約機能は実装中です。')
    
    return render(request, 'accounts/premium_cancel.html')


@login_required
def delete_account_view(request):
    """アカウント削除ページ"""
    if request.method == 'POST':
        messages.info(request, 'アカウント削除機能は実装中です。')
    
    return render(request, 'accounts/delete_account.html')
