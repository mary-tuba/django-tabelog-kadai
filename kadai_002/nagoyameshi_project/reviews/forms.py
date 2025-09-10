from django import forms
from .models import Review
from restaurants.models import Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewCreateForm(forms.ModelForm):
    """レビュー作成フォーム（プレミアムユーザー限定）"""
    
    rating = forms.ChoiceField(
        label='評価',
        choices=[(i, f'{i}★') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        help_text='1つ星（最低）から5つ星（最高）で評価してください'
    )
    
    comment = forms.CharField(
        label='コメント',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'お店の感想、料理の味、接客、雰囲気などを詳しくお聞かせください（任意）'
        }),
        help_text='レビューコメントは任意です。他のお客様の参考になるような内容をお願いします。'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        """評価のバリデーション"""
        rating = self.cleaned_data.get('rating')
        if rating:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise forms.ValidationError('評価は1から5の間で選択してください。')
        return rating

    def clean_comment(self):
        """コメントのバリデーション"""
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) > 1000:
            raise forms.ValidationError('コメントは1000文字以内で入力してください。')
        return comment


class AdminReviewCreateForm(forms.ModelForm):
    """管理者用レビュー作成フォーム"""
    
    user = forms.ModelChoiceField(
        label='ユーザー',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='レビューを投稿するユーザーを選択してください'
    )
    
    restaurant = forms.ModelChoiceField(
        label='店舗',
        queryset=Restaurant.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='レビュー対象の店舗を選択してください'
    )
    
    rating = forms.ChoiceField(
        label='評価',
        choices=[(i, f'{i}★') for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='1つ星（最低）から5つ星（最高）で評価してください'
    )
    
    comment = forms.CharField(
        label='コメント',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'レビューコメントを入力してください（任意）'
        }),
        help_text='レビューコメントは任意です。'
    )
    
    is_public = forms.BooleanField(
        label='公開状態',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='チェックすると公開状態になります'
    )

    class Meta:
        model = Review
        fields = ['user', 'restaurant', 'rating', 'comment', 'is_public']

    def clean_rating(self):
        """評価のバリデーション"""
        rating = self.cleaned_data.get('rating')
        if rating:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise forms.ValidationError('評価は1から5の間で選択してください。')
        return rating

    def clean_comment(self):
        """コメントのバリデーション"""
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) > 1000:
            raise forms.ValidationError('コメントは1000文字以内で入力してください。')
        return comment
    
    def clean(self):
        """重複チェック"""
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        restaurant = cleaned_data.get('restaurant')
        
        if user and restaurant:
            # 編集時は既存のレビューを除外
            existing_review = Review.objects.filter(user=user, restaurant=restaurant)
            if self.instance.pk:
                existing_review = existing_review.exclude(pk=self.instance.pk)
            
            if existing_review.exists():
                raise forms.ValidationError('この ユーザーは既にこの店舗にレビューを投稿しています。')
        
        return cleaned_data