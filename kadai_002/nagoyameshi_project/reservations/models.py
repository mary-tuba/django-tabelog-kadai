from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from restaurants.models import Restaurant


class Reservation(models.Model):
    """予約モデル"""
    
    STATUS_CHOICES = [
        ('pending', '予約中'),
        ('confirmed', '確定'),
        ('cancelled', 'キャンセル'),
        ('completed', '完了'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='ユーザー', 
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        verbose_name='店舗', 
        on_delete=models.CASCADE
    )
    
    # 予約情報
    reservation_date = models.DateField('予約日')
    reservation_time = models.TimeField('予約時間')
    party_size = models.PositiveIntegerField(
        '人数',
        validators=[MinValueValidator(1)],
        default=2
    )
    
    # 特記事項
    notes = models.TextField('特記事項', blank=True)
    
    # ステータス
    status = models.CharField(
        'ステータス', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    # 連絡先（念のため）
    contact_phone = models.CharField('連絡先電話番号', max_length=15, blank=True)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'
        ordering = ['-reservation_date', '-reservation_time']
    
    def __str__(self):
        return f'{self.restaurant.name} - {self.user.username} ({self.reservation_date} {self.reservation_time})'
    
    @property
    def is_past(self):
        """予約日時が過去かどうか"""
        from django.utils import timezone
        import datetime
        
        reservation_datetime = datetime.datetime.combine(
            self.reservation_date, 
            self.reservation_time
        )
        return timezone.make_aware(reservation_datetime) < timezone.now()
    
    @property
    def can_cancel(self):
        """キャンセル可能かどうか（予約日の1日前まで）"""
        from django.utils import timezone
        import datetime
        
        if self.status in ['cancelled', 'completed']:
            return False
            
        cancel_deadline = self.reservation_date - datetime.timedelta(days=1)
        return timezone.now().date() <= cancel_deadline
