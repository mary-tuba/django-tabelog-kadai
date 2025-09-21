from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime, timedelta
from django.utils import timezone


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


class EmailVerificationToken(models.Model):
    """メール認証用トークンモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        """トークンの有効期限切れをチェック（24時間）"""
        return timezone.now() > self.created_at + timedelta(hours=24)
    
    class Meta:
        verbose_name = 'メール認証トークン'
        verbose_name_plural = 'メール認証トークン'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.token}"
