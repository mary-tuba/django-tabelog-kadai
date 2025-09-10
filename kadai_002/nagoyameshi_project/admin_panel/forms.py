from django import forms
from .models import CompanyInfo


class CompanyInfoForm(forms.ModelForm):
    """運営会社情報編集フォーム"""
    
    company_name = forms.CharField(
        label='会社名',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        label='住所',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    phone = forms.CharField(
        label='電話番号',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    business_hours = forms.CharField(
        label='営業時間',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    established = forms.CharField(
        label='設立',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    capital = forms.CharField(
        label='資本金',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    representative = forms.CharField(
        label='代表取締役',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    business_content = forms.CharField(
        label='事業内容',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = CompanyInfo
        exclude = ['updated_at']