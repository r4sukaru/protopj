from django.urls import path
from django.conf.urls import url
from . import views


# どのアプリのurlsなのか分かるようにapp_nameを使用する。
app_name = 'searchapp'

urlpatterns = [
    #path('',views.Search.as_view(),name='search'),
    #path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('', views.ResultList.as_view(), name='result'),
    #path('', views.DetailsView.as_view(), name='details'),
]
