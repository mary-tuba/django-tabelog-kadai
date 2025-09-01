from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """カスタムユーザーモデルの管理画面設定"""
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'is_premium', 'email_verified', 'is_staff', 'date_joined'
    )
    list_filter = (
        'is_premium', 'email_verified', 'is_staff', 
        'is_superuser', 'is_active', 'date_joined'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # フィールドセット（詳細画面でのフィールド配置）
    fieldsets = UserAdmin.fieldsets + (
        ('追加情報', {
            'fields': (
                'furigana', 'postal_code', 'address', 
                'phone_number', 'is_premium', 'email_verified'
            )
        }),
    )
    
    # 新規作成時のフィールドセット
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('追加情報', {
            'fields': (
                'furigana', 'postal_code', 'address', 
                'phone_number', 'is_premium', 'email_verified'
            )
        }),
    )
