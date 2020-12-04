"""zky_file URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import  serve
from django.conf.urls.static import static
from django.contrib.auth.views import login,logout
# from index import views as up_view
from  index import views as down_view
from  esutil import  views as esview
import  os
from  index import  views as search_views
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^search/',include('search.urls')),
    # url(r'^search',include('haystack.urls')),
    url(r'^search/', search_views.MySeachView(),name='search'),
    url(r'^file/', include('file.urls')),
    url(r'^index/',include('index.urls')),
    url(r'^download',down_view.download_file,name='down_url'),
    url(r'^es',esview.essearch,name='es_url'),
    # url(r'^info/'),include('search.urls'),


    # url(r'^accounts/login/$', login, ),
    url(r'^login',search_views.acc_login,name='login'),
    url(r'^logout', search_views.acc_logout, name='logout'),
]
