"""protopjのアプリurl設定"""
from django.urls import path
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    path('',views.Search.as_view(),name='search'),
    path('result/', views.ResultList.as_view(), name='result'),
    path('details/', views.DetailsList.as_view(), name='details'),
]
