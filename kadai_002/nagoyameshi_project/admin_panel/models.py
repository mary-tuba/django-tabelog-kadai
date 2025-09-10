from django.db import models


class CompanyInfo(models.Model):
    """運営会社情報"""
    company_name = models.CharField('会社名', max_length=100, default='NAGOYA MESHI株式会社')
    address = models.TextField('住所', default='〒460-0008 愛知県名古屋市中区栄3-15-33')
    phone = models.CharField('電話番号', max_length=20, default='052-123-4567')
    email = models.EmailField('メールアドレス', default='info@nagoyameshi.com')
    business_hours = models.CharField('営業時間', max_length=50, default='平日 9:00-18:00')
    established = models.CharField('設立', max_length=20, default='2020年4月')
    capital = models.CharField('資本金', max_length=30, default='1,000万円')
    representative = models.CharField('代表取締役', max_length=50, default='名古屋 太郎')
    business_content = models.TextField('事業内容', default='飲食店情報サイトの運営\nグルメ情報の提供\nレストラン予約サービス')
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '運営会社情報'
        verbose_name_plural = '運営会社情報'
    
    def __str__(self):
        return self.company_name
    
    @classmethod
    def get_instance(cls):
        """シングルトンパターンで運営会社情報を取得"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
