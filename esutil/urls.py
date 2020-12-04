#coding:utf-8
__author__ = 'sjf'

from  views import essearch
from django.conf.urls import url
urlpatterns = [
# #     # 配置文件下载
    url(r'^(.*)$', essearch()),
]