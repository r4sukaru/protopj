"""protopjのアプリurl設定"""
from django.urls import path
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    # 指定しない場合にviewクラス(Search)を呼び出す。
    path('',views.Search.as_view(),name='search'),
    # 'result/'を指定した場合にviewクラス(ResultList)を呼び出す。
    path('result/', views.ResultList.as_view(), name='result'),
    # 'details/'を指定した場合にviewクラス(DetailsList)を呼び出す。
    path('details/', views.DetailsList.as_view(), name='details'),
]
