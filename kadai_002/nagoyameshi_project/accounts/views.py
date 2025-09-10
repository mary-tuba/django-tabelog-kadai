from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm, UserProfileForm, CustomPasswordChangeForm, AccountDeletionForm


def login_view(request):
    """ログインページ"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # デバッグ用ログ追加
        print(f"Login attempt - Username: {username}, Password length: {len(password) if password else 0}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログインしました。')
                return redirect('restaurants:index')
            else:
                messages.error(request, 'アカウントが無効化されています。')
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # ユーザーを作成
            user = form.save()
            
            # 自動ログイン（バックエンドを明示的に指定）
            login(request, user, backend='accounts.backends.EmailBackend')
            
            messages.success(request, f'{user.username}さん、会員登録が完了しました！')
            return redirect('restaurants:index')
        else:
            # フォームエラーがある場合
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    """プロフィール表示ページ"""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit_view(request):
    """プロフィール編集ページ"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('accounts:profile')
        else:
            # フォームエラーがある場合
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def password_change_view(request):
    """パスワード変更ページ"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # パスワード変更後も自動的にログイン状態を維持
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'パスワードが正常に変更されました。')
            return redirect('accounts:profile')
        else:
            # フォームエラーがある場合
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/password_change.html', {'form': form})


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
        form = AccountDeletionForm(request.user, request.POST)
        if form.is_valid():
            # 退会理由がある場合はログに記録（実際のアプリでは適切なログ管理を行う）
            reason = form.cleaned_data.get('reason')
            username = request.user.username
            if reason:
                print(f"退会理由 - ユーザー {username}: {reason}")
            
            # ユーザーアカウントを削除（削除前にuserオブジェクトを保持）
            user_to_delete = request.user
            logout(request)  # ログアウト
            user_to_delete.delete()  # アカウント削除
            
            messages.success(request, '退会手続きが完了しました。ご利用ありがとうございました。')
            return redirect('restaurants:index')
        else:
            # フォームエラーがある場合
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = AccountDeletionForm(request.user)
    
    return render(request, 'accounts/delete_account.html', {'form': form})
