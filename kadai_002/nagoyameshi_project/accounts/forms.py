from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """カスタムユーザー作成フォーム"""
    
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        label='名',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='姓',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    furigana = forms.CharField(
        label='フリガナ',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    agree_terms = forms.BooleanField(
        label='利用規約に同意する',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'furigana', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # usernameフィールドを削除
        if 'username' in self.fields:
            del self.fields['username']
        
        # フォームフィールドにBootstrapクラスを追加
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # ラベルを日本語に変更
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認）'

    def clean_email(self):
        """メールアドレスの重複チェック"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email

    def save(self, commit=True):
        """ユーザー保存時の処理"""
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        
        # メールアドレスをusernameとして設定
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.furigana = self.cleaned_data['furigana']
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """ユーザープロフィール編集フォーム"""
    
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        label='名',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='姓',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    furigana = forms.CharField(
        label='フリガナ',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    postal_code = forms.CharField(
        label='郵便番号',
        max_length=8,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567'})
    )
    
    address = forms.CharField(
        label='住所',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    phone_number = forms.CharField(
        label='電話番号',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '090-1234-5678'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'furigana', 'postal_code', 'address', 'phone_number')

    def clean_email(self):
        """メールアドレスの重複チェック（現在のユーザー以外）"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('このメールアドレスは既に他のユーザーによって使用されています。')
        return email

    def save(self, commit=True):
        """プロフィール保存時の処理"""
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        
        # メールアドレスが変更された場合、usernameも更新
        if user.email != email:
            user.username = email
            user.email = email
        
        if commit:
            user.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    """カスタムパスワード変更フォーム"""
    
    old_password = forms.CharField(
        label='現在のパスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    new_password1 = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    new_password2 = forms.CharField(
        label='新しいパスワード（確認）',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ヘルプテキストを日本語に変更
        self.fields['new_password1'].help_text = (
            "・8文字以上で入力してください\n"
            "・よくあるパスワードは使用できません\n"
            "・数字のみのパスワードは使用できません\n"
            "・現在のパスワードと似すぎているものは使用できません"
        )


class AccountDeletionForm(forms.Form):
    """退会用フォーム"""
    
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='セキュリティのため、現在のパスワードを入力してください'
    )
    
    confirm_deletion = forms.BooleanField(
        label='退会について理解しました',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='退会すると、アカウントと関連するデータが全て削除されます'
    )
    
    reason = forms.CharField(
        label='退会理由（任意）',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'サービスの改善のため、よろしければ退会理由をお聞かせください'}),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        """パスワードの認証チェック"""
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('パスワードが正しくありません。')
        return password