# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from  django.contrib.auth.models import  User
# Create your models here.


# class file(models.Model):
#     choices=(
#         (u'1',u'普通文件'),
#         (u'2', u'excel表文件'),
#         (u'3',u'图片'),
#     )
#     file = models.FileField(verbose_name='文件',max_length=254,null=True,blank=True,unique=True)#,upload_to=upload_path_handler)
#     filename = models.CharField(verbose_name='文件名',max_length=254,null=True,blank=True,unique=True)
#     # sheet_name = models.CharField(null=True, max_length=256, blank=True,unique=False,verbose_name='excel表内部表名')
#     category = models.CharField(choices=choices,blank=True,null=True,max_length=30,verbose_name='文件种类')
#     image = models.ImageField(u'图片',blank=True,null=True)
#     content=models.TextField(null=True,blank=True,default='',verbose_name='文件内容')
#     add_date = models.DateTimeField(verbose_name='上传日期',auto_now_add=True)
#     username = models.ForeignKey(User,null=True,blank=True,verbose_name='上传者',default='1')
#     # down_url = models.CharField(verbose_name='下载链接',max_length=512)
#     def __repr__(self):
#         return u'self.filename'
#
#     class Meta:
#         verbose_name = '文件'
#         verbose_name_plural = '文件'

class all_file(models.Model):
    choices=(
        (u'1',u'普通文件'),
        (u'2', u'excel表文件'),
        (u'3',u'图片'),
    )
    # up_choices = (
    #     (u'1', u'上传成功后数据未写入数据库'),
    #     (u'2', u'上传成功后数据已写入数据库'),
    # )

    # file = models.FileField(verbose_name='文件',max_length=256,null=False,blank=False,unique=True)#,upload_to=upload_path_handler)
    filename = models.CharField(verbose_name='文件名',max_length=254,null=True,blank=True,unique=True)
    # sheet_name = models.CharField(null=True, max_length=256, blank=True,unique=False,verbose_name='excel表内部表名')
    category = models.CharField(choices=choices,blank=True,null=True,max_length=30,verbose_name='文件种类')
    # image = models.ImageField(u'图片',blank=True,null=True)
    content=models.TextField(null=True,blank=True,default='',verbose_name='文件内容')
    add_date = models.DateTimeField(verbose_name='上传日期',auto_now_add=True)
    username = models.ForeignKey(User,null=True,blank=True,verbose_name='上传者',default='1')
    # up_status = models.CharField(choices=up_choices,verbose_name=u'文件上传状态',default=1,max_length=10)
    # down_url = models.CharField(verbose_name='下载链接',max_length=512)
    def __repr__(self):
        return u'self.filename'

    class Meta:
        verbose_name = '文件总表'
        verbose_name_plural = '文件总表'




class excel(models.Model):
    # id=models.IntegerField(primary_key=True)
    sheet_name =models.CharField(null=True,max_length=254,blank=True)
    excel_name = models.ForeignKey(all_file,max_length=254,blank=True,null=True,verbose_name='表文件名',to_field='filename')
    # excel_content = models.TextField(max_length=1000000,null=True,blank=True,verbose_name='表单的内容')
    add_date = models.DateTimeField(verbose_name='上传日期', auto_now_add=True)
    username = models.ForeignKey(User, null=True, blank=True, verbose_name='上传者')
    li_name=models.CharField(max_length=256,default='')
    li_ctx=models.CharField(max_length=10000,null=True,blank=True,verbose_name='该列内容')
    li_num=models.IntegerField(verbose_name='列号',default=0)
    row_num=models.IntegerField(verbose_name='行号',default=0)
    unit_mark=models.IntegerField(blank=True,default='')
    def __repr__(self):
        return u'self.excel_name'

    class Meta:
        verbose_name = '表内容'
        verbose_name_plural = '表内容'
        # unique_together = ('excel_name_id','li_ctx','row_num','li_num')

class field(models.Model):
    field_name = models.CharField(max_length=254,verbose_name='列名',unique=True)
    field_val = models.CharField(max_length=254,verbose_name='每个字段的value值',default='')
    add_date = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return u'self.field_name'
    class Meta:
        ordering= ['add_date']
        verbose_name = '列名'
        verbose_name_plural = '列名'

