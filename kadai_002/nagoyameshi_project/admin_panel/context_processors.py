from .models import CompanyInfo


def company_info(request):
    """運営会社情報をテンプレートで利用できるようにするコンテキストプロセッサー"""
    return {
        'company_info': CompanyInfo.get_instance()
    }