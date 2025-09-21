from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ユーザー認証
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # ユーザー管理
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
    
    # プレミアム会員関連
    path('premium/upgrade/', views.premium_upgrade_view, name='premium_upgrade'),
    path('premium/cancel/', views.premium_cancel_view, name='premium_cancel'),
    
    # 退会
    path('delete/', views.delete_account_view, name='delete_account'),
    
    # メール認証
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
    path('verify/resend/', views.resend_verification, name='resend_verification'),
]