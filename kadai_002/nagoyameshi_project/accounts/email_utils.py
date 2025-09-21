from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import EmailVerificationToken


def send_verification_email(request, user, token):
    """認証メールを送信"""
    subject = '【NAGOYAMESHI】メールアドレスの認証'
    
    # 認証URLの生成
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={'token': token.token})
    )
    
    # メール本文
    message = f"""
    {user.username}様

    NAGOYAMESHIへのご登録ありがとうございます。

    以下のリンクをクリックしてメールアドレスを認証してください：
    {verification_url}

    このリンクは24時間有効です。

    ※このメールに心当たりがない場合は、破棄してください。

    --
    NAGOYAMESHI
    """
    
    # HTML版のメール（オプション）
    html_message = f"""
    <h3>{user.username}様</h3>
    <p>NAGOYAMESHIへのご登録ありがとうございます。</p>
    <p>以下のボタンをクリックしてメールアドレスを認証してください：</p>
    <p style="margin: 30px 0;">
        <a href="{verification_url}" 
           style="background-color: #007bff; color: white; padding: 10px 20px; 
                  text-decoration: none; border-radius: 5px;">
            メールアドレスを認証
        </a>
    </p>
    <p>またはこちらのURLにアクセス：<br>
    <a href="{verification_url}">{verification_url}</a></p>
    <p style="color: #666;">このリンクは24時間有効です。</p>
    <hr>
    <p style="color: #999; font-size: 12px;">
    ※このメールに心当たりがない場合は、破棄してください。
    </p>
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False