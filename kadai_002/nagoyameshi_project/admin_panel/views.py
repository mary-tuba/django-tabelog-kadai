from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Count
from django.db import models
import csv
from django.http import HttpResponse
from django.utils import timezone
from accounts.forms import CustomUserCreationForm
from restaurants.models import Restaurant
from reviews.models import Review
from reservations.models import Reservation
from categories.models import Category
from .models import CompanyInfo
from .forms import CompanyInfoForm

User = get_user_model()


@staff_member_required
def dashboard(request):
    """管理者ダッシュボード"""
    # 統計データの取得
    total_users = User.objects.count()
    total_restaurants = Restaurant.objects.count()
    total_reviews = Review.objects.count()
    total_reservations = Reservation.objects.count()
    
    # 最近の登録ユーザー（5件）
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # 最近のレビュー（5件）
    recent_reviews = Review.objects.select_related('user', 'restaurant').order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_restaurants': total_restaurants,
        'total_reviews': total_reviews,
        'total_reservations': total_reservations,
        'recent_users': recent_users,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

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
    """会員管理 - ユーザー一覧"""
    # 検索・フィルタリング機能
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    user_type_filter = request.GET.get('user_type', 'all')
    
    # ベースクエリ
    users = User.objects.all().order_by('-date_joined')
    
    # 検索機能
    if search_query:
        users = users.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    
    # ステータスフィルター
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # ユーザータイプフィルター
    if user_type_filter == 'admin':
        users = users.filter(is_staff=True)
    elif user_type_filter == 'premium':
        users = users.filter(is_premium=True)
    elif user_type_filter == 'regular':
        users = users.filter(is_staff=False, is_premium=False)
    
    # ページネーション
    from django.core.paginator import Paginator
    paginator = Paginator(users, 20)  # 1ページに20人表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 統計情報
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    premium_users = User.objects.filter(is_premium=True).count()
    admin_users = User.objects.filter(is_staff=True).count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'user_type_filter': user_type_filter,
        'total_users': total_users,
        'active_users': active_users,
        'premium_users': premium_users,
        'admin_users': admin_users,
    }
    
    return render(request, 'admin_panel/user_list.html', context)

@staff_member_required
def user_detail(request, user_id):
    """会員詳細"""
    user = get_object_or_404(User, id=user_id)
    
    # ユーザーの関連データを取得
    user_reviews = Review.objects.filter(user=user).select_related('restaurant').order_by('-created_at')[:10]
    user_reservations = Reservation.objects.filter(user=user).select_related('restaurant').order_by('-created_at')[:10]
    user_favorites = user.favorites.select_related('restaurant').order_by('-created_at')[:10] if hasattr(user, 'favorites') else []
    
    # 統計情報
    review_count = Review.objects.filter(user=user).count()
    reservation_count = Reservation.objects.filter(user=user).count()
    favorite_count = user.favorites.count() if hasattr(user, 'favorites') else 0
    
    context = {
        'user_obj': user,  # userという名前は予約済みなのでuser_objとする
        'user_reviews': user_reviews,
        'user_reservations': user_reservations,
        'user_favorites': user_favorites,
        'review_count': review_count,
        'reservation_count': reservation_count,
        'favorite_count': favorite_count,
    }
    
    return render(request, 'admin_panel/user_detail.html', context)

@staff_member_required
def user_delete(request, user_id):
    """会員削除"""
    target_user = get_object_or_404(User, id=user_id)
    
    # 自分自身の削除は防ぐ
    if target_user == request.user:
        messages.error(request, '自分自身のアカウントを削除することはできません。')
        return redirect('admin_panel:user_list')
    
    # スーパーユーザーの削除に追加の確認
    if target_user.is_superuser:
        if not request.POST.get('confirm_superuser_delete'):
            return render(request, 'admin_panel/user_delete_confirm.html', {
                'target_user': target_user,
                'is_superuser': True
            })
    
    if request.method == 'POST':
        username = target_user.username
        user_id = target_user.id
        
        # 関連データの統計を取得
        review_count = Review.objects.filter(user=target_user).count()
        reservation_count = Reservation.objects.filter(user=target_user).count()
        favorite_count = target_user.favorites.count() if hasattr(target_user, 'favorites') else 0
        
        # ユーザーとその関連データを削除
        target_user.delete()
        
        messages.success(
            request, 
            f'ユーザー「{username}」(ID: {user_id})を削除しました。'
            f'関連データ: レビュー{review_count}件、予約{reservation_count}件、お気に入り{favorite_count}件も削除されました。'
        )
        return redirect('admin_panel:user_list')
    
    # GET リクエスト時は確認ページを表示
    return render(request, 'admin_panel/user_delete_confirm.html', {
        'target_user': target_user,
        'is_superuser': target_user.is_superuser
    })

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


# 管理者管理機能
@staff_member_required
def admin_user_create(request):
    """管理者ユーザー作成"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 管理者権限を付与
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f'管理者ユーザー「{user.username}」を作成しました。')
            return redirect('admin_panel:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'admin_panel/admin_user_create.html', {'form': form})


@staff_member_required
def regular_user_create(request):
    """一般ユーザー作成"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'一般ユーザー「{user.username}」を作成しました。')
            return redirect('admin_panel:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'admin_panel/regular_user_create.html', {'form': form})


@staff_member_required
def admin_logout(request):
    """管理者ログアウト"""
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('restaurants:index')


@staff_member_required
def admin_password_change(request):
    """管理者パスワード変更"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # パスワード変更後もログイン状態を維持
            update_session_auth_hash(request, request.user)
            messages.success(request, 'パスワードが正常に変更されました。')
            return redirect('admin_panel:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'admin_panel/admin_password_change.html', {'form': form})


@staff_member_required
def company_info_edit(request):
    """運営会社情報編集"""
    company = CompanyInfo.get_instance()
    
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, '運営会社情報を更新しました。')
            return redirect('admin_panel:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = CompanyInfoForm(instance=company)
    
    return render(request, 'admin_panel/company_info_edit.html', {'form': form, 'company': company})


@staff_member_required
def user_password_reset(request, user_id):
    """管理者によるユーザーパスワードリセット"""
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            if len(new_password) >= 8:
                target_user.set_password(new_password)
                target_user.save()
                messages.success(request, f'ユーザー「{target_user.username}」のパスワードを変更しました。')
                return redirect('admin_panel:user_detail', user_id=user_id)
            else:
                messages.error(request, 'パスワードは8文字以上で入力してください。')
        else:
            messages.error(request, 'パスワードが一致しません。')
    
    return render(request, 'admin_panel/user_password_reset.html', {'target_user': target_user})


@staff_member_required
def user_status_toggle(request, user_id):
    """ユーザーのアクティブ状態を切り替え"""
    target_user = get_object_or_404(User, id=user_id)
    
    # 自分自身の無効化は防ぐ
    if target_user == request.user:
        messages.error(request, '自分自身のアカウントを無効化することはできません。')
        return redirect('admin_panel:user_detail', user_id=user_id)
    
    if request.method == 'POST':
        target_user.is_active = not target_user.is_active
        target_user.save()
        
        status_text = 'アクティブ' if target_user.is_active else '無効'
        messages.success(request, f'ユーザー「{target_user.username}」を{status_text}にしました。')
    
    return redirect('admin_panel:user_detail', user_id=user_id)


@staff_member_required
def user_premium_toggle(request, user_id):
    """ユーザーのプレミアム状態を切り替え"""
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # is_premiumフィールドが存在するかチェック
        if hasattr(target_user, 'is_premium'):
            target_user.is_premium = not target_user.is_premium
            target_user.save()
            
            status_text = 'プレミアム' if target_user.is_premium else '一般'
            messages.success(request, f'ユーザー「{target_user.username}」を{status_text}会員にしました。')
        else:
            messages.error(request, 'プレミアム機能が利用できません。')
    
    return redirect('admin_panel:user_detail', user_id=user_id)


@staff_member_required
def user_list_csv_export(request):
    """会員一覧のCSVエクスポート"""
    # 同じフィルタリング機能を適用
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    user_type_filter = request.GET.get('user_type', 'all')
    
    # ベースクエリ
    users = User.objects.all().order_by('-date_joined')
    
    # 検索機能
    if search_query:
        users = users.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    
    # ステータスフィルター
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # ユーザータイプフィルター
    if user_type_filter == 'admin':
        users = users.filter(is_staff=True)
    elif user_type_filter == 'premium':
        users = users.filter(is_premium=True)
    elif user_type_filter == 'regular':
        users = users.filter(is_staff=False, is_premium=False)
    
    # CSVレスポンスの準備
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    current_time = timezone.now().strftime('%Y%m%d_%H%M%S')
    
    # フィルター条件をファイル名に反映
    filename_parts = ['会員一覧']
    if search_query:
        filename_parts.append(f'検索_{search_query}')
    if status_filter != 'all':
        status_name = {'active': 'アクティブ', 'inactive': '無効'}[status_filter]
        filename_parts.append(status_name)
    if user_type_filter != 'all':
        type_name = {'admin': '管理者', 'premium': 'プレミアム', 'regular': '一般'}[user_type_filter]
        filename_parts.append(type_name)
    
    filename = f"{'_'.join(filename_parts)}_{current_time}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # BOMを追加（Excel での文字化け防止）
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # ヘッダー行
    headers = [
        'ID',
        'ユーザー名',
        '姓',
        '名',
        'フリガナ',
        'メールアドレス',
        '電話番号',
        '郵便番号',
        '住所',
        '会員タイプ',
        'ステータス',
        'プレミアム会員',
        'スタッフ権限',
        'スーパーユーザー',
        '登録日',
        '最終ログイン',
        'レビュー数',
        '予約数',
        'お気に入り数'
    ]
    writer.writerow(headers)
    
    # データ行
    for user in users:
        # 会員タイプの判定
        if user.is_staff:
            user_type = '管理者'
        elif getattr(user, 'is_premium', False):
            user_type = 'プレミアム'
        else:
            user_type = '一般'
        
        # ステータスの判定
        status = 'アクティブ' if user.is_active else '無効'
        
        # 関連データの数を取得
        review_count = Review.objects.filter(user=user).count()
        reservation_count = Reservation.objects.filter(user=user).count()
        favorite_count = user.favorites.count() if hasattr(user, 'favorites') else 0
        
        # 日付のフォーマット
        date_joined = user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else ''
        last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '未ログイン'
        
        row = [
            user.id,
            user.username,
            user.last_name or '',
            user.first_name or '',
            getattr(user, 'furigana', '') or '',
            user.email,
            getattr(user, 'phone_number', '') or '',
            getattr(user, 'postal_code', '') or '',
            getattr(user, 'address', '') or '',
            user_type,
            status,
            '○' if getattr(user, 'is_premium', False) else '',
            '○' if user.is_staff else '',
            '○' if user.is_superuser else '',
            date_joined,
            last_login,
            review_count,
            reservation_count,
            favorite_count
        ]
        writer.writerow(row)
    
    # エクスポート実行のログをメッセージで通知
    export_count = users.count()
    messages.success(request, f'{export_count}件の会員データをCSVエクスポートしました。')
    
    return response


# カテゴリ管理機能
@staff_member_required
def category_list(request):
    """カテゴリ一覧"""
    categories = Category.objects.all().order_by('name')
    
    context = {
        'categories': categories,
        'total_categories': categories.count(),
    }
    
    return render(request, 'admin_panel/category_list.html', context)


@staff_member_required
def category_create(request):
    """カテゴリ作成"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name:
            try:
                category = Category.objects.create(
                    name=name,
                    description=description
                )
                messages.success(request, f'カテゴリ「{category.name}」を作成しました。')
                return redirect('admin_panel:category_list')
            except Exception as e:
                if 'UNIQUE constraint failed' in str(e) or 'duplicate key value' in str(e):
                    messages.error(request, f'カテゴリ名「{name}」は既に存在します。')
                else:
                    messages.error(request, f'カテゴリの作成に失敗しました: {str(e)}')
        else:
            messages.error(request, 'カテゴリ名を入力してください。')
    
    return render(request, 'admin_panel/category_create.html')


@staff_member_required
def category_edit(request, category_id):
    """カテゴリ編集"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name:
            try:
                category.name = name
                category.description = description
                category.save()
                messages.success(request, f'カテゴリ「{category.name}」を更新しました。')
                return redirect('admin_panel:category_list')
            except Exception as e:
                if 'UNIQUE constraint failed' in str(e) or 'duplicate key value' in str(e):
                    messages.error(request, f'カテゴリ名「{name}」は既に存在します。')
                else:
                    messages.error(request, f'カテゴリの更新に失敗しました: {str(e)}')
        else:
            messages.error(request, 'カテゴリ名を入力してください。')
    
    context = {
        'category': category
    }
    
    return render(request, 'admin_panel/category_edit.html', context)


@staff_member_required
def category_delete(request, category_id):
    """カテゴリ削除"""
    category = get_object_or_404(Category, id=category_id)
    
    # 関連する店舗があるかチェック
    related_restaurants = Restaurant.objects.filter(category=category)
    restaurant_count = related_restaurants.count()
    
    if request.method == 'POST':
        if restaurant_count > 0 and not request.POST.get('force_delete'):
            messages.error(request, f'このカテゴリは{restaurant_count}店舗で使用されているため削除できません。')
            return redirect('admin_panel:category_delete', category_id=category_id)
        
        category_name = category.name
        category.delete()
        
        if restaurant_count > 0:
            messages.warning(request, f'カテゴリ「{category_name}」を削除しました。関連する{restaurant_count}店舗のカテゴリ情報も削除されました。')
        else:
            messages.success(request, f'カテゴリ「{category_name}」を削除しました。')
        
        return redirect('admin_panel:category_list')
    
    context = {
        'category': category,
        'related_restaurants': related_restaurants,
        'restaurant_count': restaurant_count,
    }
    
    return render(request, 'admin_panel/category_delete.html', context)