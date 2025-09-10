from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator
from accounts.decorators import premium_required
from restaurants.models import Restaurant
from .models import Reservation
from .forms import ReservationCreateForm


@premium_required()
def create_reservation(request, restaurant_id):
    """予約作成（プレミアムユーザー限定）"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    
    if request.method == 'POST':
        form = ReservationCreateForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.restaurant = restaurant
                reservation.status = 'pending'
                reservation.save()
                messages.success(request, f'「{restaurant.name}」のご予約を承りました。確認のご連絡をお待ちください。')
                return redirect('reservations:detail', reservation_id=reservation.id)
            except IntegrityError:
                messages.error(request, '予約の作成中にエラーが発生しました。')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = ReservationCreateForm()
    
    context = {
        'form': form,
        'restaurant': restaurant,
    }
    return render(request, 'reservations/create.html', context)


@premium_required()
def reservation_list(request):
    """予約一覧（プレミアムユーザー限定）"""
    reservations = Reservation.objects.filter(user=request.user).select_related('restaurant').order_by('-reservation_date', '-reservation_time')
    
    # ページネーション
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'reservations/list.html', context)


@premium_required()
def reservation_detail(request, reservation_id):
    """予約詳細（プレミアムユーザー限定）"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/detail.html', context)


@premium_required()
def cancel_reservation(request, reservation_id):
    """予約キャンセル（プレミアムユーザー限定）"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # キャンセル可能かチェック
    if not reservation.can_cancel:
        messages.error(request, 'この予約はキャンセルできません。')
        return redirect('reservations:detail', reservation_id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f'「{reservation.restaurant.name}」の予約をキャンセルしました。')
        return redirect('reservations:list')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/cancel.html', context)