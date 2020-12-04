# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  haystack.urls import SearchView
  # import

def info(req,sheet_name,row_num):

    return  render(req,'includes/info.html')


# Create your views here.
# class  MySeachView(SearchView):
#     # def extra_context(self):  # 重载extra_context来添加额外的context内容
#     #     # context = super(MySeachView, self).extra_context()
#     #     # request = super(MySeachView,self).request()
#     #     template = super(MySeachView,self).template()
#     #     template = 'includes/search.html'
#     #     # side_list = {''}
#     #     # context['search_option'] = side_list
#     #     # return context
#     #     return  template
#     def create_response(self):
#         # pass
#         # if self.request.method == 'GET':
#
#         self.context = self.get_context()
#         self.context['search_option'] = [{'remark_name': '2', 'name': '3'},
#                                     {'remark_name': '5', 'name': '6'}]
#         # context['query'] = str(self.request.POST.get('q')) + str(self.request.POST.get('q'))
#         # print  context['query']
#         if  'search_kinds' in self.request.GET:
#             # self.context['search_val'] = self.request.GET('search_kinds')
#             '''
#             name标签
#             '''
#             self.context['query'] = str(self.request.GET.get('q'))  + str(self.request.GET('search_kinds'))
#
#         return  render(self.request,self.template,self.context)
#         # elif self.request.method == 'POST':
#         #     context = {}
#         #     # context['search_option'] = [{'value': '1', 'remark_name': '2', 'name': '3'},
#         #     #                             {'value': '4', 'remark_name': '5', 'name': '6'}]
#         #     # context['query'] =  self.request.POST.get('q') + self.request.POST.get('q')
#         # context['page'] = self.page
#         #     return render(self.request, self.template, context)
#     # context={}


'''
select distinct 查询字段名   from 表名;
'''