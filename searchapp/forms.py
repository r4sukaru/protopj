"""フォーム"""
from django import forms


class GoodSearchForm(forms.Form):
    """検索用フォーム"""

    goods = forms.CharField(
        initial='',
        label='商品名',
        required=False,
        )
    category = forms.CharField(
        initial='',
        label='カテゴリ名',
        required=False,
        )
    price = forms.IntegerField(
        initial='',
        label='価格',
        required=False,
        )
    '''
    highcategory = forms.CharField(
        initial='',
        label='上位カテゴリ名',
        required=False,
        )
    '''
