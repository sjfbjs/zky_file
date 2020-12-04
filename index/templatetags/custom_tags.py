# -*- coding:utf-8 -*-
# Author:Alex Li
from django import template
from django.utils.html import format_html
from index.models import field
import  xlwt,xlrd
# fd=field
# print fd.objects.all()
register = template.Library()

@register.filter
def alex_upper(val):
    print("--val from template:",val )
    return val.upper()


@register.simple_tag
def guess_page(current_page,loop_num):
    offset = abs(current_page - loop_num)
    if offset <3:
        if current_page == loop_num:
            page_ele = '''<li class="active"><a href="?page=%s">%s</a></li>''' %(loop_num,loop_num)
        else:
            page_ele = '''<li class=""><a href="?page=%s">%s</a></li>''' %(loop_num,loop_num)
        return format_html(page_ele)
    else:
        return ''


# IP='123.207.92.55'
# IP='127.0.0.1'
# PORT=8000

from  django.conf import settings

import  os,json
from django.conf import  settings



@register.simple_tag
def    find_content(row_num,sheet_name,fn):
    # import re, os, commands
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    fpath = os.path.join(settings.MEDIA_ROOT, str(fn).decode('utf-8', 'ignore'))
    # ctx=commands.getoutput("grep -rnH '%s' %s" %(query.decode('utf-8','ignore'),str(fn).decode('utf-8','ignore')))
    '''这边对文件做一个判断'''
    # print fn
    fname, ext = fn.split('.')
    if ext == 'xls' or ext == 'xlsx':

        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        import xlrd
        if os.path.exists(fpath):
            workbook = xlrd.open_workbook(fpath)

            # all_data = []
            row_val = []
            # sheet_name = workbook.sheet_names()[0]
            sheet = workbook.sheet_by_name(sheet_name)
            # ctx = sheet.row_values(row_num)
            fields=sheet.row_values(0)
            fd = field
            '''这边用有序列表来做'''
            fd_na = fd.objects.values('field_name')
            # fds_name=[]
            p_tt = ''
            '''这边就是有序的'''
            Rmark_na='<td  style="text-align:middle; vertical-align:middle; ">\</td>'

            unit_rema='<td  style="text-align:middle; vertical-align:middle; ">\</td>'

            pic_hre = '<td  style="text-align:middle; vertical-align:middle; ">' \
                      '<h5 >' \
                      '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>'%(settings.IP,settings.PORT)
            # xu1_hre = '<td  style="text-align:middle; vertical-align:middle; ">' \
            #           '<h5 >' \
            #           '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>'%(settings.IP,settings.PORT)
            # xu2_hre = '<td  style="text-align:middle; vertical-align:middle; ">' \
            #           '<h5 >' \
            #           '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>'%(settings.IP,settings.PORT)
            # xu3_hre = '<td  style="text-align:middle; vertical-align:middle; ">' \
            #           '<h5 >' \
            #           '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>'%(settings.IP,settings.PORT)



            '''zip包表头列表，这边的表头有点多，用html元素来做这个添加'''
            llist = ['COI', 'COI-2', 'COIII', '12S', '16S', '18S', '28S', 'H3', 'WNT', 'L494',
                     'L168', 'ND1', 'Actin5c', '12-16S', 'EF1a', 'AK', 'GAPDH', 'Nak', 'PEPCK',
                     'PDI', 'HSP', '转录组', '张鹏']

            '''html标签列表'''

            meta_list = ['li','dl',
                         'dt','dd',
                         'p','ul',
                         'ol','label',
                         'datalist','option',
                         'summary','select',
                         'optgroup','textarea',
                         'video','source',
                         'caption',
                         'meta','b',
                         'pre',
                         'title','dir',
                         'menu','code',
                         'small','big',
                         ]


            # for  ob in  llist:
            #     ob_hre = '<td  style="text-align:middle; vertical-align:middle; ">' '<h5 >' '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>' % (
            #               settings.IP, settings.PORT)

            oth_href=' '
            # print  fd_na
            for obj in fd_na:
                for k, v in obj.items():
                    if v.decode('utf-8') in fields:
                        if   v.decode('utf-8') != '统一编号':
                            # print 'index:%s'%fields.index(v)
                            p_tt  +=  '<td style="text-align:middle; vertical-align:middle; ">%s</td>'  % sheet.cell_value(row_num,fields.index(v.decode('utf-8')))

                        else:
                            '重写'
                            # if v.decode('utf-8') == u'标本编号':
                            #     Rmark_na ='<td style="text-align:middle; vertical-align:middle; ">%s</td>' % sheet.cell_value(row_num,fields.index(v.decode('utf-8')))
                            if  v.decode('utf-8')  ==  u'统一编号':
                                xu_num = sheet.cell_value(row_num,fields.index(v.decode('utf-8')))
                                # xu_num = xu_num.decode('utf-8').split('IOZ')[1]
                                # print 'xu_num : %s' %xu_num
                                unit_rema = '<td style="text-align:middle; vertical-align:middle; ">%s</td>' \
                                            % \
                                            sheet.cell_value(row_num,fields.index(v.decode('utf-8')))
                                # xu1_zip_name  = '序列1'+xu_num+'.zip'
                                # xu2_zip_name = '序列2'+xu_num+'.zip'
                                # xu3_zip_name = '序列3'+xu_num+'.zip'
                                pic_zip_name = '形态照片'+xu_num+'.zip'

                                for ob in  llist:
                                    ob_zip_name = ob+xu_num+'.zip'
                                    ob_path = os.path.join(settings.MEDIA_ROOT,ob_zip_name)
                                    # print 'ob_path : %s' %ob_path
                                    # print  'ob_path:%s' %ob_path
                                    '''这块代码有问题'''
                                    if  os.path.exists(ob_path):
                                        # print  'ob_index : %s' % llist.index(ob)
                                        print  '<td  style="text-align:middle; vertical-align:middle; background:yellow;"><%s><input  value="%s" name="%s" type="checkbox" id="%s"></%s><a href="http://%s:%s/file/%s">%s</a></td>' % (meta_list[llist.index(ob)],xu_num,ob,ob,meta_list[llist.index(ob)],settings.IP,settings.PORT,ob_zip_name,ob)
                                        ob_hre = '<td  style="text-align:middle; vertical-align:middle; background:yellow;"><%s><input  value="%s" name="%s" type="checkbox" id="%s"></%s><a href="http://%s:%s/file/%s">%s</a></td>' % (meta_list[llist.index(ob)],xu_num,ob,ob,meta_list[llist.index(ob)],settings.IP,settings.PORT,ob_zip_name,ob)
                                        # ob_hre = ''
                                        # print  'ob_hre : %s' %ob_hre
                                    else:
                                        ob_hre = '<td  style="text-align:middle; vertical-align:middle; ">' '<h5 >' '<a href="http://%s:%s/index/upload" style="color:red">未上传</a></h5></td>' % (
                                            settings.IP, settings.PORT)
                                    oth_href += ob_hre


                                # print 'ob_href:%s' % oth_href
                                # xu1_path = os.path.join(settings.MEDIA_ROOT, xu1_zip_name)
                                # xu2_path = os.path.join(settings.MEDIA_ROOT, xu2_zip_name)
                                # xu3_path = os.path.join(settings.MEDIA_ROOT, xu3_zip_name)
                                # if os.path.exists(xu1_path):
                                #     xu1_hre = '<td  style="text-align:middle; vertical-align:middle; background:yellow;">' \
                                #               '<i   style="nowrap" ><input  value="%s" name="xu1s" type="checkbox" id="xu1s">' \
                                #               '<a href="http://%s:%s/file/%s">序列1</a></i></td>' % (xu_num,settings.IP,settings.PORT,xu1_zip_name)
                                # if os.path.exists(xu2_path):
                                #     xu2_hre = '<td  style="text-align:middle; vertical-align:middle; background:yellow;">' \
                                #               '<sub id=序列2><input  value="%s" name="xu2s" type="checkbox" id="xu2s"></sub>' \
                                #               '<a href="http://%s:%s/file/%s">序列2</a></td>' %\
                                #         (
                                #         xu_num,
                                #         settings.IP,
                                #         settings.PORT,
                                #         xu2_zip_name
                                #         )
                                # if os.path.exists(xu3_path):
                                #     xu3_hre = '<td  style="text-align:middle; vertical-align:middle; background:yellow;">' \
                                #               '<sup  id=序列3><input  value="%s" name="xu3s" type="checkbox" id="xu3s"></sup>' \
                                #               '<a href="http://%s:%s/file/%s">序列3</a></td>' % \
                                #               (
                                #                   xu_num,
                                #                   settings.IP,
                                #                   settings.PORT,
                                #                   xu3_zip_name
                                #               )

                                pic_path= os.path.join(settings.MEDIA_ROOT,pic_zip_name)
                                if os.path.exists(pic_path):
                                    pic_hre = '<td  style="text-align:middle; vertical-align:middle;background:yellow; ">' \
                                              '<strong id=图片><input  value="%s" name="pics" type="checkbox" id="pics"></strong>' \
                                              '<a href="http://%s:%s/file/%s">图片</a></td>' % \
                                              (
                                               xu_num,
                                               settings.IP,
                                               settings.PORT,
                                               pic_zip_name
                                              )


                    else:
                        p_tt += '<td  style="text-align:middle; vertical-align:middle; ">\</td>'

            hre='<td  style="text-align:left; vertical-align:middle; "><a href="http://%s:%s/index/%s/%s/%s"><h5 >%s</h5></a></td>' %(settings.IP,settings.PORT, fn, sheet_name, int(row_num)+1, fname)

            # print hre
            return   format_html('<tr >'+'<td style="text-align:left; vertical-align:middle; "> <input  value=%s_%s name="downloads" type="checkbox" id="down"></td>'%(fn,row_num)+unit_rema+p_tt+hre+pic_hre+oth_href+'</tr>' )
            print    '<tr >'+'<td style="text-align:left; vertical-align:middle; "> <input  value=%s_%s name="downloads" type="checkbox" id="down"></td>'%(fn,row_num)+unit_rema+p_tt+hre+pic_hre+x1_hre+'</tr>'

        else:
            return  ''

# @register.simple_tag
# def   guss_permissions(req):
@register.simple_tag
def   category(num):
    dict1 = {'1':u'普通文件',
            '2':u'Excel',
            '3':u'图片'
            }
    if num :
        return  dict1[num]
    else:
        return


# from django.urls.html import  format_html
@register.simple_tag
def row_content_deal(ctx):



    ctx = ctx.replace('[', '').replace(']', '')
    # ctx = unicodedata.normalize('NFKD', ctx).encode('utf-8', 'ignore')
    ctx = ctx.split(',')
    ctx_List = []
    for i in range(len(ctx)):

        ctx_List.append(ctx[i])
    # print ctx_List
    ct_list=[]
    import  json
    if ctx_List:
        r_ctx=''
        for obj in ctx_List:
            # print obj.replace("'","")
            print json.loads(obj.replace("'",""))
            for k,v in json.loads(obj.replace("'","")).items():
                r_ctx +=  ' <'+k.decode('unicode_escape','ignore')+ ":"+str(v).decode('unicode_escape','ignore')+' '+'> '
            # print "k:%s,v:%s" %(k.decode('unicode_escape','ignore',v))
         # ct_list.append(obj.decode('utf-8'))
        return  r_ctx
    #


