#coding:utf-8
from  views import download_file
from django.conf.urls import url
urlpatterns = [
    # 配置文件下载
    url(r'^(.*)$', download_file),
]