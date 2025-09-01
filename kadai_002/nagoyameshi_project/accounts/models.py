from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """カスタムユーザーモデル"""
    
    # 基本情報
    furigana = models.CharField('フリガナ', max_length=100, blank=True)
    postal_code = models.CharField('郵便番号', max_length=8, blank=True)
    address = models.TextField('住所', blank=True)
    phone_number = models.CharField('電話番号', max_length=15, blank=True)
    
    # プレミアム会員フラグ
    is_premium = models.BooleanField('プレミアム会員', default=False)
    
    # メール認証フラグ
    email_verified = models.BooleanField('メール認証済み', default=False)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'

    def __str__(self):
        return f"{self.username} ({self.email})"
