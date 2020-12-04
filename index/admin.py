# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,json
from django.contrib import admin
import commands
# Register your models here.
from django.contrib import admin
from  django.http import  StreamingHttpResponse
# Register your models here.
from models import all_file,excel,field
import  os,json,datetime
from  django.conf import  settings
import  xlrd,re
from django.shortcuts import render,render_to_response
from  django.contrib.auth.models import  User
import pytz
from django.core.exceptions import ValidationError




def   Space_1(modeladmin,request,queryset):
    pass

'''
项目本身就有配置不够集中的问题
像excel可以写个集中处理的方法进行调用
'''
def readFile(filename,chunk_size=512):
    with open(os.path.join(settings.MEDIA_ROOT,filename),'rb') as f:
        print settings.MEDIA_ROOT
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

def delete_allfiles(modeladmin, request, queryset):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''先删除文件，再删除记录'''
    for obj in queryset:
        fn = unicode(obj.filename)
        # print   fn
        # print settings.MEDIA_ROOT
        ''''''
        file_path=os.path.join(settings.MEDIA_ROOT,fn)
        print  file_path
        if os.name == 'nt':
            print  os.system("del  %s"%file_path )
        elif os.name == 'posix':
            print  os.system("rm -f  %s" % file_path)
        fname, ext = fn.split('.')
        if ext == 'xls' or ext == 'xlsx':
            exc = excel
            if exc.objects.filter(excel_name_id=fn):
                exc.objects.filter(excel_name_id=fn).delete()
    queryset.delete()
    '''删除excel表的所有数据'''

class allfilelist(admin.ModelAdmin):
    list_display = ('filename','add_date','username',)
    list_filter = ('filename','username')
    search_fields = ['filename','content']
    ordering = ('add_date',)
    list_per_page = 50
    # actions = [Space_1,Space_2,delete_files,download_files ,update_excel_content]
    actions = [Space_1,delete_allfiles]#,update_excel_content]

    exclude = ['content','sheet_name']
    class Meta:
        # obj=file.objects.filter(filename=)
        # f1.save()
        pass

def download_files(modeladmin, request, queryset):
    '''获取文件名'''
    for obj in queryset:
        fn = unicode(obj.filename)

        # 文件名
        print fn
        response = StreamingHttpResponse(readFile(fn))
        # response['Content-Title'] = fn
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fn)
        return response
download_files.short_description = u"下载选中文件"


import commands
def delete_files(modeladmin, request, queryset):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''先删除文件，再删除记录'''
    for obj in queryset:
        fn = unicode(obj.filename)
        # print   fn
        # print settings.MEDIA_ROOT
        ''''''
        file_path=os.path.join(settings.MEDIA_ROOT,fn)
        print  file_path
        if os.name == 'nt':
            print  os.system("del  %s"%file_path )
        elif os.name == 'posix':
            commands.getoutput("rm -f  %s" % file_path)
            # print  os.system("rm -f  %s" % file_path)
    queryset.delete()
    '''删除excel表的字段'''
delete_files.short_description = u"删除选中文件上传记录及文件,请谨慎操作"




def   Space_1(modeladmin,request,queryset):
    pass
Space_1.short_description = u"---------------"
def   Space_2(modeladmin,request,queryset):
    pass
Space_2.short_description = u"-------如有需要请执行下面的操作--------"
def   Space_3(modeladmin,request,queryset):
    pass
Space_3.short_description = u"---------------"




def   update_excel_content(modeladmin,request,queryset):
    # user=User
    # user_name=request.user.username
    # user_id=user.objects.filter(user_name).id
    # print user_id
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''先删除文件，再删除记录'''
    for obj in queryset:
        fn = unicode(obj.filename)
        f = file
        exl=excel
        fd = field
        '''遍历表单，更新数据库'''
        fname, ext = fn.split('.')
        print fname
        print ext
        if ext == 'xlsx' or ext == 'xls':
            fpath = os.path.join(settings.MEDIA_ROOT, fn)
            workbook = xlrd.open_workbook(fpath)
            # 获取所有sheet
            # print workbook.sheet_names() # [u'sheet1', u'sheet2']
            # 获取所有sheet
            all_data = []
            for sheet_name in workbook.sheet_names():
                print sheet_name
                # # 根据sheet索引或者名称获取sheet内容
                sheet = workbook.sheet_by_name(sheet_name)
                # sheet的名称，行数，列数
                print sheet.name,sheet.nrows,sheet.ncols
                # global row_val
                # row_val = []
                print  u'<<<------------------开始循环-------------->>>'
                li_list=sheet.row_values(0)
                new_list = []
                reload(sys)
                sys.setdefaultencoding('utf-8')
                for  xx in li_list:
                    reload(sys)
                    sys.setdefaultencoding('utf-8')
                    new_list.append(str(xx).decode('utf-8') )
                print new_list
                try:
                    if sheet.ncols > 0  :
                        for i in range(sheet.ncols):
                            #print new_list[i].decode('unicode-escape','ignore')
                            #print '%s---i:%s--all:%s'%(new_list[i],i,fd.objects.all())
                            #print fd.objects.all()
                            if   fd.objects.filter(field_name=new_list[i]) or new_list[i] == '' :
                                # if sheet.nrows>0:
                                for j in range(1, sheet.nrows):
                                    ctx = str(sheet.col_values(i)[j])  # .decode('unicode-escape','ignore')
                                    #print ctx
                                    # sheet_name == 'Sheet1' or sheet_name == 'Sheet2':
                                    print ctx
                                    print  '开始创建数据 %s' % sheet_name
                                    t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    # if exl.objects.filter(excel_content=ctx):
                                    #     pass
                                    # #     exl.objects.update(excel_content=ctx, sheet_name=sheet_name, excel_name_id=fn,
                                    # #                      add_date=t1,username_id='1')
                                    # else:
                                    exl.objects.create(sheet_name=sheet_name, excel_name_id=fn,
                                                           add_date=t1, username_id='1', li_ctx=ctx, li_name=new_list[i],                                                       li_num=int(i)+1, row_num=int(j)+1)
                                # else:
                                #     break
                                #return  render(request,'includes/ok.html')
                            else:
                                # continue
                                return render(request, 'includes/base.html',
                                                  context={'errstr': u'请先创建字段%s' % new_list[i]})
                    else:
                        return render(request, 'includes/base.html', context={'errstr': u'该分表%s无数据' % sheet_name})
                except IndexError as e:
                    break



                # for i in range(1,sheet.nrows):
                #     # print  sheet.row_values(i)
                #
                #     # print type(row_val)
                #     # row_val.append(sheet.row_values(i))
                #     for j in range(sheet.ncols):
                #
                #         ctx = str(sheet.row_values(i)[j])#.decode('unicode-escape','ignore')
                #         # if sheet_name == 'Sheet1' or sheet_name == 'Sheet2':
                #         print ctx
                #         t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #         # if exl.objects.filter(excel_content=ctx):
                #         #     pass
                #         # #     exl.objects.update(excel_content=ctx, sheet_name=sheet_name, excel_name_id=fn,
                #         # #                      add_date=t1,username_id='1')
                #         # else:
                #         #if sheet_name == 'Sheet1' or sheet_name == 'Sheet2':
                #         print  '开始创建数据 %s' %sheet_name
                #         if  exl.objects.filter(sheet_name=sheet_name,excel_name_id=fn,li_ctx=ctx,row_num=i+1,li_num=j+1):
                #             pass
                #         else:
                #             exl.objects.create(sheet_name=sheet_name, excel_name_id=fn,
                #                              add_date=t1 ,username_id='1',li_ctx=ctx,li_name=li_list[j],li_num=j+1,row_num=i+1)
                    # print row_val
                # print row_val
                '''这边上面跑通了，但是这边没过去'''
                # global ex_content
                # ex_content = {}
                # # print type(ex_content)
                # ex_content[sheet_name] = str(row_val)
                # all_data.append(ex_content)
            # sheets_name=workbook.sheet_names()
        # print all_data
        '''处理数据库数据'''
        # if  f.objects.filter(str(all_data)):
        #     pass
        # else:
        # for sheet_name in  sheets_name:
        #     print sheet_name
        #     for  obj in all_data:
        #         # print obj
        #         print type(obj)
        #         for k,v in obj.items():
        #             # print k
        #             if  k==sheet_name:
        #                 print k
        #                 # f.objects.
        #                 t1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        # if  f.objects.filter(sheet_name=unicode(sheet_name)):
                        #     f.objects.update(content=obj[sheet_name],sheet_name=unicode(sheet_name),filename=fn,add_date=t1,category='2')
                        # else:
                        #     f.objects.create(content=obj[sheet_name],sheet_name=unicode(sheet_name),filename=fn,image='',add_date=t1,category='2',)
    return  render(request,'includes/ok.html')
update_excel_content.short_description = u'更新excel表文件数据'


def   update_excel_ctx(modeladmin,request,queryset):
    # user=User
    # user_name=request.user.username
    # user_id=user.objects.filter(user_name).id
    # print user_id
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''先删除文件，再删除记录'''
    for obj in queryset:
        fn = unicode(obj.excel_name)
        f = excel
        f1=file
        '''遍历表单，更新数据库'''
        fname, ext = fn.split('.')
        if ext == 'xlsx' or ext == 'xls':
            fpath = os.path.join(settings.MEDIA_ROOT, fn)
            if os.path.exists(fpath):
                workbook = xlrd.open_workbook(fpath)
                # 获取所有sheet
                # print workbook.sheet_names() # [u'sheet1', u'sheet2']
                # 获取所有sheet
                for sheet_name in workbook.sheet_names():

                    sheet = workbook.sheet_by_name(sheet_name)
                    # sheet的名称，行数，列数
                    # print sheet.name,sheet.nrows,sheet.ncols


                    for i in range(sheet.nrows):
                        # print type(row_val)

                        ctx=sheet.row_values(i)
                        t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if f1.objects.filter(filename=fn):
                            if f.objects.filter(excel_content=str(ctx)):
                                f.objects.update(excel_content=str(ctx), sheet_name=unicode(sheet_name), excel_name=fn,
                                             add_date=t1, category='2')
                            else:
                                f.objects.create(excel_content=str(ctx), sheet_name=unicode(sheet_name), excel_name=fn, image='',
                                             add_date=t1, category='2', )
                        # print row_val
                        '''这边上面跑通了，但是这边没过去'''
            else:
                break
update_excel_ctx.short_description = u'更新excel表每行数据'



class filelist(admin.ModelAdmin):
    list_display = ('filename','add_date','username',)
    list_filter = ('filename','username')
    search_fields = ['filename','content']
    ordering = ('add_date',)
    list_per_page = 50
    # actions = [Space_1,Space_2,delete_files,download_files ,update_excel_content]
    actions = [Space_2,delete_files,update_excel_content]

    exclude = ['content','sheet_name']
    class Meta:
        # obj=file.objects.filter(filename=)
        # f1.save()
        pass


class excellist(admin.ModelAdmin):
    list_display = ('excel_name_id','username', 'add_date', 'li_ctx',)
    # search_fields = ['excel_name_id', 'li_ctx']
    ordering = ('add_date',)
    list_per_page = 50
    # actions =  [update_excel_ctx,]
    # actions = [Space_1,Space_2,Space_3,delete_files,download_files]
    class Meta:
        pass

class  fieldlist(admin.ModelAdmin):
     list_display =  ('field_name','field_val')
     list_filter = ('field_name',)
     class Meta:
         pass


class MyModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(request,self).get_actions()
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(all_file,allfilelist)
admin.site.register(excel,excellist)
admin.site.register(field,fieldlist)



# admin_site = MyAdminSite(name='management')

admin.site.site_header = '文件管理系统'
admin.site.site_title = '文件管理系统'
