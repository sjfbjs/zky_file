#coding:utf-8
import datetime
from haystack import indexes
from models import   excel
import  os

# class FileIndex(indexes.SearchIndex, indexes.Indexable):
#     filename = indexes.CharField(use_template=True)
#     image = indexes.CharField(use_template=True)
#     text = indexes.CharField(document=True, use_template=True)
#
#     def get_model(self):
#         return file
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()



class ExcelIndex(indexes.SearchIndex,indexes.Indexable):
    excel_name = indexes.CharField(use_template=True)
    li_name = indexes.CharField(use_template=True)
    # li_ctx = indexes.CharField(use_template=True)
    li_num = indexes.IntegerField(use_template=True)
    row_num = indexes.IntegerField(use_template=True)
    unit_mark = indexes.IntegerField(use_template=True)
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return excel

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return  self.get_model().objects.all().ordered
        '''在这边处理排序，效果不太好'''
        return self.get_model().objects.all().order_by('unit_mark')