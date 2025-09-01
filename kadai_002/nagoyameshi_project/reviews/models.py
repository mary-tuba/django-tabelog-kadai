from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from restaurants.models import Restaurant


class Review(models.Model):
    """レビューモデル"""
    
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
    
    # レビュー内容
    rating = models.PositiveIntegerField(
        '評価',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1-5の星評価'
    )
    comment = models.TextField('コメント', blank=True)
    
    # 公開状態
    is_public = models.BooleanField('公開', default=True)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'
        ordering = ['-created_at']
        # 1ユーザー1店舗につき1レビュー
        unique_together = [['user', 'restaurant']]
    
    def __str__(self):
        return f'{self.restaurant.name} - {self.user.username} ({self.rating}★)'
    
    @property
    def star_display(self):
        """星表示用"""
        return '★' * self.rating + '☆' * (5 - self.rating)
