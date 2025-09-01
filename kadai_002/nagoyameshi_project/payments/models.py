from django.db import models
from django.conf import settings


class Subscription(models.Model):
    """サブスクリプションモデル"""
    
    STATUS_CHOICES = [
        ('active', 'アクティブ'),
        ('cancelled', 'キャンセル'),
        ('expired', '期限切れ'),
        ('payment_failed', '決済失敗'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    
    # Stripe関連情報
    stripe_customer_id = models.CharField('Stripe顧客ID', max_length=100, blank=True)
    stripe_subscription_id = models.CharField('StripeサブスクリプションID', max_length=100, blank=True)
    
    # サブスクリプション情報
    status = models.CharField(
        'ステータス',
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    current_period_start = models.DateTimeField('現在の期間開始日', null=True, blank=True)
    current_period_end = models.DateTimeField('現在の期間終了日', null=True, blank=True)
    
    # 金額（月額300円）
    amount = models.PositiveIntegerField('月額料金', default=300)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'サブスクリプション'
        verbose_name_plural = 'サブスクリプション'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.get_status_display()}'
    
    @property
    def is_active(self):
        """アクティブなサブスクリプションかどうか"""
        from django.utils import timezone
        return (
            self.status == 'active' and 
            self.current_period_end and 
            self.current_period_end > timezone.now()
        )


class PaymentHistory(models.Model):
    """決済履歴モデル"""
    
    STATUS_CHOICES = [
        ('pending', '処理中'),
        ('succeeded', '成功'),
        ('failed', '失敗'),
        ('cancelled', 'キャンセル'),
    ]
    
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='サブスクリプション',
        on_delete=models.CASCADE,
        related_name='payment_history'
    )
    
    # Stripe関連情報
    stripe_payment_intent_id = models.CharField('Stripe決済ID', max_length=100, blank=True)
    
    # 決済情報
    amount = models.PositiveIntegerField('金額')
    status = models.CharField(
        'ステータス',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # 決済日時
    payment_date = models.DateTimeField('決済日時', null=True, blank=True)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '決済履歴'
        verbose_name_plural = '決済履歴'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.subscription.user.username} - ¥{self.amount} ({self.get_status_display()})'
