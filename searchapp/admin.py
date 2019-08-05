"""Djangoの管理サイトに関する記述を設定"""
from django.contrib import admin
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL

# Register your models here.
'''
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goodsid','categoryname','sizename','colorname','goodsname')
    def categoryname(self,obj):
        return obj.categoryid.categoryname
    categoryname.short_description = 'categoryname'
'''
# 管理者ページで表示させる処理
admin.site.register(GoodsTBL)
admin.site.register(CategoryTBL)
admin.site.register(HighCategoryTBL)