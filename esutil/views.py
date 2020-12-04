# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

def  essearch(req):
    if 'search_kinds' in req.GET:
        pass
    url = 'http://192.168.0.252:9200/'
    client = Elasticsearch(url)
    index_list = []
    resl=[]
    for index  in index_list :
        try:
            s = Search(using=client, index=index).query('match', columnname="__all__").filter("range", **{'@timestamp': {"from": "now-1000d", "lt": "now"}})
            response = s.execute()
            resl.append(response)
            for hit in response['hits']['hits']:
                print(hit['_source'])

        except Exception as e:
            print("Error: " + str(e))
    return  HttpResponse(resl)