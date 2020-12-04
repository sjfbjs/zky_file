# coding:utf-8
from django.conf.urls import url
from  views import info,upload,index
from  views import download_file
urlpatterns = [
    # 配置文件下载
    # url(r'^index',index),
    url(r'^upload$', upload,name='upload'),
    # url(r'^/(.*)/(\d+)',info,name='info' ),
    url(r'^(.*)/(.*)/(\d+)$', info),
    # url(r'^file/(.*)', download_file),
]