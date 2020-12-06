# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from  tasks import  Test
def  essearch(req):
    if 'search_kinds' in req.GET:
        pass
    Test.apply_async(args=("C:\\sofitware",), queue='work_queue')
    # Test.delay()
    return  HttpResponse("ok")