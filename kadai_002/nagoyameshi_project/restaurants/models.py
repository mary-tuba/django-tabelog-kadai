from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from categories.models import Category


class Restaurant(models.Model):
    """店舗モデル"""
    
    # 基本情報
    name = models.CharField('店舗名', max_length=100)
    description = models.TextField('説明', blank=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    
    # 住所・連絡先
    postal_code = models.CharField('郵便番号', max_length=8, blank=True)
    address = models.TextField('住所')
    phone_number = models.CharField('電話番号', max_length=15, blank=True)
    
    # 営業情報
    opening_hours = models.CharField('営業時間', max_length=100, blank=True)
    closed_days = models.CharField('定休日', max_length=100, blank=True)
    
    # 予算情報（円）
    budget_min = models.PositiveIntegerField(
        '予算下限', 
        validators=[MinValueValidator(0)], 
        default=0,
        help_text='最低予算（円）'
    )
    budget_max = models.PositiveIntegerField(
        '予算上限', 
        validators=[MinValueValidator(0)], 
        default=5000,
        help_text='最高予算（円）'
    )
    
    # 画像
    image = models.ImageField('メイン画像', upload_to='restaurants/', blank=True, null=True)
    
    # 公開状態
    is_active = models.BooleanField('公開中', default=True)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '店舗'
        verbose_name_plural = '店舗'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('restaurants:detail', kwargs={'restaurant_id': self.pk})
    
    @property
    def average_rating(self):
        """平均評価を計算"""
        reviews = self.review_set.filter(is_public=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0
    
    @property
    def review_count(self):
        """レビュー数を取得"""
        return self.review_set.filter(is_public=True).count()


class Favorite(models.Model):
    """お気に入りモデル"""
    
    user = models.ForeignKey(
        'accounts.User', 
        verbose_name='ユーザー', 
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        verbose_name='店舗', 
        on_delete=models.CASCADE
    )
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り'
        ordering = ['-created_at']
        # 1ユーザー1店舗につき1お気に入り
        unique_together = [['user', 'restaurant']]
    
    def __str__(self):
        return f'{self.user.username} - {self.restaurant.name}'
