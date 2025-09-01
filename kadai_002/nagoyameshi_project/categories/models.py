from django.db import models


class Category(models.Model):
    """料理カテゴリモデル"""
    
    name = models.CharField('カテゴリ名', max_length=50, unique=True)
    description = models.TextField('説明', blank=True)
    
    # 作成・更新日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['name']
    
    def __str__(self):
        return self.name
