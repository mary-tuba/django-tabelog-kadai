from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Reservation
import datetime


class ReservationCreateForm(forms.ModelForm):
    """予約作成フォーム"""
    
    reservation_date = forms.DateField(
        label='予約日',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat(),
        }),
        help_text='予約したい日付を選択してください'
    )
    
    reservation_time = forms.TimeField(
        label='予約時間',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        help_text='予約したい時間を選択してください（例：18:30）'
    )
    
    party_size = forms.IntegerField(
        label='人数',
        min_value=1,
        max_value=10,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 10,
        }),
        help_text='1～10名まで選択できます'
    )
    
    contact_phone = forms.CharField(
        label='連絡先電話番号',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '080-1234-5678',
        }),
        help_text='緊急連絡先として使用します（任意）'
    )
    
    notes = forms.CharField(
        label='特記事項',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'アレルギー、座席の希望、その他ご要望がございましたらご記入ください',
        }),
        help_text='アレルギーや特別なご要望がありましたらお知らせください（任意）'
    )

    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size', 'contact_phone', 'notes']

    def clean_reservation_date(self):
        """予約日のバリデーション"""
        reservation_date = self.cleaned_data.get('reservation_date')
        if reservation_date:
            if reservation_date < timezone.now().date():
                raise ValidationError('過去の日付は選択できません。')
            
            # 3ヶ月先まで予約可能
            max_date = timezone.now().date() + datetime.timedelta(days=90)
            if reservation_date > max_date:
                raise ValidationError('3ヶ月先までの日付を選択してください。')
                
        return reservation_date

    def clean_reservation_time(self):
        """予約時間のバリデーション"""
        reservation_time = self.cleaned_data.get('reservation_time')
        if reservation_time:
            # 営業時間内かチェック（例：11:00-22:00）
            open_time = datetime.time(11, 0)
            close_time = datetime.time(22, 0)
            
            if reservation_time < open_time or reservation_time > close_time:
                raise ValidationError('営業時間内（11:00-22:00）の時間を選択してください。')
                
        return reservation_time

    def clean(self):
        """全体のバリデーション"""
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        reservation_time = cleaned_data.get('reservation_time')
        
        # 現在時刻より未来かチェック
        if reservation_date and reservation_time:
            reservation_datetime = datetime.datetime.combine(reservation_date, reservation_time)
            now = timezone.now()
            
            # タイムゾーンを考慮した比較
            reservation_datetime = timezone.make_aware(reservation_datetime)
            
            if reservation_datetime <= now + datetime.timedelta(hours=1):
                raise ValidationError('予約は1時間後以降の時間を選択してください。')
        
        return cleaned_data