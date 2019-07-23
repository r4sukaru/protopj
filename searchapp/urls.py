from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    #path('',views.Search.as_view(),name='search'),
    path('', views.ResultList.as_view(), name='result'),
    path('details/', views.DetailsList.as_view(), name='details'),
    #path('post/<int:pk>/', views.Details_View.as_view(), name='details'),
    #path('post/', views.DetailsList.as_view(), name='details'),
]
