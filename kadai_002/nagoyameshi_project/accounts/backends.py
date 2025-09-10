from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    メールアドレスでのログインを可能にするカスタム認証バックエンド
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # usernameにメールアドレスが入力された場合
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # 従来のusernameでも認証可能にする（下位互換性）
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None