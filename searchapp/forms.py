"""
内部構成
class CategorySearchField
    def label_from_instance
class CategorySearchForm
class GoodsSearchForm
"""
from django import forms

from .models import CategoryTBL


class CategorySearchField(forms.ModelChoiceField):
    """
    プルダウンフォームを表示するためのModelChoiceFormを継承したクラス
    label_from_instanceでプルダウンの値を上書きしている（？）
    """
    def label_from_instance(self, obj=CategoryTBL):
        return f"{obj.categoryname}"


class CategorySearchForm(forms.Form):
    """
    この中で↑のモデルを呼びだしてカテゴリプルダウンとして使用する
    """
    category_name = CategorySearchField(
        label='',
        required=False,
        queryset=CategoryTBL.objects.all(),
        empty_label='カテゴリ',
    )


class GoodsSearchForm(forms.Form):
    """
    フリーワード検索のフォームを表示する為のクラス
    """

    search_char = forms.CharField(
        max_length=100,
        initial='',
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'フリーワード検索', 'class': 'class_name'
                }
        )
    )
