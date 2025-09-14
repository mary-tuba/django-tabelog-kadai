from django import forms
from .models import Restaurant
from categories.models import Category


class RestaurantCreateForm(forms.ModelForm):
    """プレミアム会員用 店舗追加フォーム"""
    
    name = forms.CharField(
        label='店舗名',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'レストラン名を入力してください'
        })
    )
    
    description = forms.CharField(
        label='店舗説明',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '店舗の特徴や雰囲気、おすすめ料理などを入力してください'
        })
    )
    
    category = forms.ModelChoiceField(
        label='カテゴリ',
        queryset=Category.objects.all(),
        empty_label='カテゴリを選択してください',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    postal_code = forms.CharField(
        label='郵便番号',
        max_length=8,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567（ハイフンなし）'
        })
    )
    
    address = forms.CharField(
        label='住所',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': '都道府県から番地まで入力してください'
        })
    )
    
    phone_number = forms.CharField(
        label='電話番号',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '03-1234-5678'
        })
    )
    
    opening_hours = forms.CharField(
        label='営業時間',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '11:00-22:00 (L.O.21:30)'
        })
    )
    
    closed_days = forms.CharField(
        label='定休日',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '毎週月曜日、第3日曜日'
        })
    )
    
    budget_min = forms.IntegerField(
        label='予算下限（円）',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1000',
            'step': '100'
        })
    )
    
    budget_max = forms.IntegerField(
        label='予算上限（円）',
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '3000',
            'step': '100'
        })
    )
    
    website_url = forms.URLField(
        label='ウェブサイト',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com'
        })
    )
    
    image = forms.ImageField(
        label='店舗画像',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='推奨サイズ: 800x600px、最大5MB'
    )

    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'category', 'image', 'postal_code', 'address', 
            'phone_number', 'opening_hours', 'closed_days', 
            'budget_min', 'budget_max', 'website_url'
        ]

    def clean(self):
        """フォーム全体のバリデーション"""
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        
        # 空の予算値をデフォルト値に設定
        if budget_min is None or budget_min == '':
            cleaned_data['budget_min'] = 0
            budget_min = 0
        if budget_max is None or budget_max == '':
            cleaned_data['budget_max'] = 5000
            budget_max = 5000
        
        # 予算の整合性チェック
        if budget_min is not None and budget_max is not None:
            if budget_min > budget_max:
                raise forms.ValidationError('予算下限は予算上限以下で設定してください。')
        
        return cleaned_data
    
    def clean_postal_code(self):
        """郵便番号のバリデーション"""
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code:
            # ハイフンを除去
            postal_code = postal_code.replace('-', '')
            # 7桁の数字チェック
            if not postal_code.isdigit() or len(postal_code) != 7:
                raise forms.ValidationError('郵便番号は7桁の数字で入力してください（例: 1234567）')
        return postal_code
    
    def save(self, commit=True):
        """保存時の処理"""
        restaurant = super().save(commit=False)
        
        # 予算の空の値をデフォルト値で置き換え
        if restaurant.budget_min is None:
            restaurant.budget_min = 0
        if restaurant.budget_max is None:
            restaurant.budget_max = 5000
        
        # 承認待ち状態で保存（管理者が承認するまで非公開）
        restaurant.is_active = False  # 管理者承認待ち
        
        if commit:
            restaurant.save()
        return restaurant