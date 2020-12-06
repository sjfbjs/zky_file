# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,redirect,HttpResponse
from collections import OrderedDict
from  models import  field
# from
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from  django.conf import  settings
import  os,xlrd,xlwt,time,sys,re,commands
# Create your views here.
# from  forms import  IndexModelForm
from django.contrib.auth import  authenticate,login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.html import format_html

# print settings.IP
# print settings.PORT




@csrf_exempt
def  acc_logout(req):
    return  render(req,'includes/logout.html')


@csrf_exempt
def   acc_login(req):
    if req.method == 'POST':
        print  "acc_login"
        user = authenticate(username=req.POST.get('username'),
                           password = req.POST.get('password'),)
        print   req.POST.get('username')
        print   req.POST.get('password')
        if user is not None:
            login(req,user)
            # return HttpResponseRedirect('/search')
            return  redirect('/search')
        else:
            login_err=u'您输入的用户名或者密码不正确'
            return  render(req,'registration/login.html',{"login_err":login_err})
    return  render(req,'registration/login.html')

@csrf_exempt
def info(req,file_name,sheet_name,row_num):
    fpath = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(fpath):
        workbook = xlrd.open_workbook(fpath)
        sheet = workbook.sheet_by_name(sheet_name)
        li_nu = sheet.ncols
        row_first = sheet.row_values(0)
        row_val = sheet.row_values(int(row_num)-1)
        objs={}
        for i in  range(li_nu):
            objs[row_first[i]] = row_val[i]
        # objs=excel.objects.values('li_ctx').get(sheet_name=sheet_name,row_num=row_num,excel_name_id=file_name)
        # print str(objs).decode('utf-8')
        # form = IndexModelForm(instance=objs)
        return  render(req,'includes/info.html',{'objs':objs})
    else:
        return  HttpResponse(u'对不起，这个文件不存在！')



from tasks import  EsImportFromFile,Test
from  models import  all_file,excel,field
import random,string,datetime
@csrf_exempt
# @login_required

def upload(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''这个函数集中处理上传的文件'''
    file_model = all_file
    up_history = file_model.objects.all()
    # up_history = ''

    if request.method == 'GET':
        #return render(request, 'includes/upload.html',context={'up_history':up_history,'IP':settings.IP,'PORT':settings.PORT})
        if  up_history and up_history != None:
    	    return render(request, 'includes/upload.html',context={'up_history':up_history,'IP':settings.IP,'PORT':settings.PORT})
        else:
	    return render(request, 'includes/upload.html')

    elif request.method == "POST":
        objs = request.FILES.getlist('myfiles')
        t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if objs:
            # print(obj.name,obj.size)  #读取文件名称和大小，返回后台，这块需要改下
            for obj in objs:
                # print obj.name
                fpath = os.path.join(settings.MEDIA_ROOT,obj.name)
                # print fpath
                if  os.path.exists(fpath):
                    fn, ext = obj.name.split('.')
                    if ext == 'xls' or ext == 'xlsx':
                        return render(request, 'includes/upload.html', context={'up_err': u'<-  %s  ->该文件名已经存在，请更改文件名或者后台删除该文件后再进行上传'%obj.name})
                        break
                    elif  ext == 'zip':
                        '''先删除再创建'''
                        commands.getoutput(' rm -rf  %s' %(fpath))
                        f = open(fpath, 'wb')
                        for chunk in obj.chunks():
                            f.write(chunk)
                            #f.close()
                        # file_model.objects.create(filename=obj.name,
                        #                           category=u'1',
                        #                           content='zip',
                        #                           add_date=t1,
                        #                           username_id='1')



                else:
                    '''开始写入数据库'''
                    Test.apply_async(args=(fpath,), queue='work_queue')
                    exc = excel
                    fd = field
                    if file_model.objects.filter(filename=obj.name) or exc.objects.filter(excel_name_id=obj.name):
                        return render(request, 'includes/upload.html',
                                      context={'up_err': u'<-  %s  ->数据库内容已经存在，请更改文件名或者在后台删除该文件所有数据库记录后再进行上传' % obj.name})
                        break
                    else:
                        '''读取excel的时候excel不能手动打开，不然会报错'''
                        f = open(fpath, 'wb')
                        for chunk in obj.chunks():
                            f.write(chunk)
                            #f.close()


                        fn,ext = obj.name.split('.')
                        if ext == 'xls' or ext =='xlsx':
                            file_model.objects.create(filename=obj.name,
                                                      category=u'2',
                                                      content='',
                                                      add_date=t1,
                                                      username_id='1')
                            workbook = xlrd.open_workbook(fpath)
                            all_data = []
                            if len(workbook.sheet_names()) > 0:
                                sheet_name = workbook.sheet_names()[0]
                                # print sheet_name
                                # # 根据sheet索引或者名称获取sheet内容
                                sheet = workbook.sheet_by_name(sheet_name)
                                # sheet的名称，行数，列数
                                # print sheet.name, sheet.nrows, sheet.ncols

                                # print  u'<<<------------------开始循环-------------->>>'
                                li_list = sheet.row_values(0)
                                new_list = []
                                reload(sys)
                                sys.setdefaultencoding('utf-8')
                                '''读取列表数据'''
                                for xx in li_list:
                                    reload(sys)
                                    sys.setdefaultencoding('utf-8')
                                    new_list.append(str(xx).decode('utf-8'))
                                    # print xx
                                    if  fd.objects.filter(field_name=xx):
                                        pass
                                    else:
                                        fd_val=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], 6)).replace(" ","")
                                        # print 'fd_val:%s' % fd_val
                                        fd.objects.create(field_name=str(xx).decode('utf-8'),field_val=fd_val)
                                # print int(sheet.nrows)-1
                                if sheet.ncols > 0:
                                    for i in range(sheet.ncols):

                                        for j in range(1, sheet.nrows):
                                            ctx = str(sheet.col_values(i)[j])  # .decode('unicode-escape','ignore')

                                            try:
                                                unit_ma = int(sheet.cell_value(j,0).split('IOZ')[1])
                                                # print 'unit_ma:%s' % unit_ma
                                            except:
                                                pass
                                            # unit_ma = int(unit_ma)
                                            # print 'unit_ma:%s' % unit_ma
                                            # print ctx
                                            # sheet_name == 'Sheet1' or sheet_name == 'Sheet2':
                                            # print ctx

                                            '''单独处理下时间这列'''
                                            if unit_ma:
                                                # print  'row_mark:%s' % sheet.cell_value(j, 0)
                                                # print  '开始创建数据 %s' % sheet_name
                                                if   '时间' in   li_list:
                                                    if i == li_list.index('时间'):
                                                        try:
                                                            yyy=re.split(r"[/ ,.-]", ctx)[0]
                                                            mmm=re.split(r"[/ ,.-]", ctx)[1]
                                                            ddd=re.split(r"[/ ,.-]", ctx)[2]
                                                        except:
                                                            yyy = '2018'
                                                            mmm = '01'
                                                            ddd = '01'
                                                        ctx = '%s年%s月%s' %(yyy,mmm,ddd)
                                                        # print  'i:%s' % i
                                                        # print 'ctx  : %s'%ctx

                                                        if sheet.cell(j, i).ctype != 2:
                                                            # pass
                                                            if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=ctx,
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                                pass
                                                            else:
                                                                exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=ctx,
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)
                                                        else:
                                                            # print  'ctx:%s'%type(ctx)
                                                            # print    type(int(float(ctx)))
                                                            if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                                pass
                                                            else:
                                                                exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                          li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)
                                                    else:
                                                        # unit_ma = str(sheet.col_values(1)[j]).split('IOZ')[1]
                                                        if sheet.cell(j, i).ctype != 2:
                                                            # pass
                                                            if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=ctx,
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                                pass
                                                            else:
                                                                exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=ctx,
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)

                                                        else:
                                                            # print  'ctx:%s'%type(ctx)
                                                            # print    type(int(float(ctx)))
                                                            if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                                pass
                                                            else:
                                                                exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                       add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                       li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)
                                                else:
                                                    if sheet.cell(j, i).ctype != 2:
                                                        # pass
                                                        if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                   add_date=t1, username_id='1', li_ctx=ctx,
                                                                                   li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                            pass
                                                        else:
                                                            exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                   add_date=t1, username_id='1', li_ctx=ctx,
                                                                                   li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)
                                                    else:
                                                        # print  'ctx:%s'%type(ctx)
                                                        # print    type(int(float(ctx)))
                                                        if  exc.objects.filter(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                   add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                   li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma):
                                                            pass
                                                        else:
                                                            exc.objects.create(sheet_name=sheet_name, excel_name_id=obj.name,
                                                                                   add_date=t1, username_id='1', li_ctx=int(float(ctx)),
                                                                                   li_name=new_list[i],li_num=i+1,row_num=j,unit_mark=unit_ma)
                        elif  ext == 'jpg' or ext == 'img' or ext =='jpeg' or ext == 'png':
                            file_model.objects.create(filename=obj.name,
                                                      category=u'3',
                                                      # content='',
                                                      add_date=t1,
                                                      username_id='1')

                            # file_model.objects.create()

                        # else:
                        #     '''这边zip包就不做上传历史记录了，只是在前面判断是否存在'''
                        #
                        #     with open(fpath,'r+') as f:
                        #         cont=f.read()
                        #     file_model.objects.create(filename=obj.name,
                        #                               category=u'1',
                        #                               content=cont,
                        #                               add_date=t1,
                        #                               username_id='1')
                            # file_model.objects.create()
            return  render(request,'includes/upload.html',context={'up_status':u'成功'})
        else:
            return  render(request,'includes/upload.html',context={'up_err':u'您还未选择需要上传的文件，请重新操作'})
        # models.Img.objects.create(path=file_path)
        '''上传的时候直接回传'''
        ret={'status':True,'path':file_path}
        # return HttpResponse(json.dumps(ret))
        return  render(request,'includes/upload.html')



@csrf_exempt
def index(req):
    return  render(req, 'includes/t1.html')


'''只能在这边把函数写在这边了，无法引用别的app'''


from  django.conf.global_settings import  MEDIA_ROOT

@csrf_exempt
def download_file(request, fn=''):

    v_list = request.POST.getlist('downloads')
    # print 'v_list:%s' %v_list
    pics_list = request.POST.getlist('pics')
    # xu1s_list = request.POST.getlist('xu1s')
    # xu2s_list = request.POST.getlist('xu2s')
    # xu3s_list = request.POST.getlist('xu3s')
    # print  v_list
    '''这边对获取到的数据进行处理'''
    '''先创建一个表文件'''
    fd=field
    fids=[]
    unit_list = []
    # fids.append('统一编号')
    # fids.append('标本编号')
    fd_na = fd.objects.values('field_name')
    '''这边就是有序的'''
    # Rmark_na = ''

    for obj in fd_na:
        for k, v in obj.items():
            fids.append(v)
    # print 'fids : %s' % fids

    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    tt = time.strftime("%Y-%m-%d_%H:%M", time.localtime())
    all_nums = len(v_list)
    for i in range(len(fids)):
        if  type(fids[i]) == str:
            sheet1.write(0, i, fids[i].decode('utf-8'))  # write的第一个,第二个参数时坐标, 第三个是要写入的数据
        else:
            sheet1.write(0, i, fids[i])  # write的第一个,第二个参数时坐标, 第三个是要写入的数据
    for  j in range(all_nums):
        fna,row_nn=v_list[j].decode('utf-8').split('_')
        # print 'd_v:%s' %row_nn
        # print  'fname:%s'%fname
        # print  'row_nn:%s'%row_nn
        for k in range(len(fids)):
            fpath = os.path.join(settings.MEDIA_ROOT,fna)
            workbook = xlrd.open_workbook(fpath)
            sheet_na = workbook.sheet_names()[0]
            sheet = workbook.sheet_by_name(sheet_na)
            # ctx = sheet.row_values(row_nn)
            fi_first = sheet.row_values(0)
            if fids[k]  in  fi_first:
                li_ctx = sheet.cell_value(int(row_nn),fi_first.index(fids[k]))
                if  fids[k] == '统一编号':
                    unit_list.append(li_ctx)
                if  type(li_ctx) == str:
                    sheet1.write(j+1,k,li_ctx.decode('utf-8'))
                else:
                    sheet1.write(j + 1, k, li_ctx)
            else:
                sheet1.write(j+1,k,"\\")
    new_exc = "temp_%s.xls"%tt
    f.save(os.path.join(settings.MEDIA_ROOT,new_exc))  # 保存文件
    all_file_name = 'all_%s.zip' %tt
    # all_zip_file =  os.path.join(settings.MEDIA_ROOT,all_file_name)
    """修改这一块下载，获取前端回传的值"""
    down_list=' '

    # for item1 in xu1s_list:
    #     down_list += ' 序列1' + str(item1) + '.zip '
    # for item2 in xu2s_list:
    #     down_list += ' 序列2' + str(item2) + '.zip '
    # for item3 in xu3s_list:
    #     down_list += ' 序列3' + str(item3) + '.zip '
    for  pic in pics_list:
        down_list +=  ' 形态照片' + str(pic) + '.zip '

    # print  'content1:%s' % down_list
    """
       add   other  zip
       for   in  ........ :
    """
    llist = ['COI', 'COI-2', 'COIII', '12S', '16S', '18S', '28S', 'H3', 'WNT', 'L494',
             'L168', 'ND1', 'Actin5c', '12-16S', 'EF1a', 'AK', 'GAPDH', 'Nak', 'PEPCK',
             'PDI', 'HSP', '转录组', '张鹏']
    for  obb in llist:
        # print   'obb:%s' %obb
        obb_list = request.POST.getlist(obb)
        '''有问题'''
        # print  'obb_list : %s' % obb_list
        for  item in obb_list:
            down_list += ' ' + str(obb) + str(item) + '.zip '

    zp_list = request.POST.getlist(u'张鹏')
    print 'zp_list : %s' %zp_list
    coi_list = request.POST.getlist('COI')
    print 'coi_list : %s' % coi_list
    """压缩命令前缀"""
    fir_ctx= 'cd  %s && zip -r %s ' % (settings.MEDIA_ROOT, all_file_name)
    # print  down_list
    # print  fir_ctx + down_list + new_exc

    commands.getoutput(fir_ctx + down_list + new_exc)

    dow_url = 'http://%s:%s/file/%s'%(settings.IP,settings.PORT,all_file_name)

    return  redirect(dow_url)




from  django.shortcuts import render
from  haystack.urls import SearchView
from  models import  field,excel
import  sys,time
from django.http import Http404
from django.core.paginator import InvalidPage, Paginator,EmptyPage
from haystack.query import SearchQuerySet
# Create your views here.
class MySeachView(SearchView):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # """

    # init_nu = 0
    def build_page(self):
        """
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError) as e:
            print e

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]
        # self.results=self.results.order_by('统一编号')
        # self.results = self.results[:]
        '''----------------用索引排序--------------------------'''
        self.results = self.results.order_by('unit_mark')
        # self.results = self.results.distinct('row_num','excel_name')
        # print  'build_page:%s' % self.results[0:]
        paginator = Paginator(self.results, self.results_per_page)
        '''这边用冒泡排序法处理results'''

        try:
            page = paginator.page(page_no)
            if len(page) > 0:
                return (paginator, page)
        except ValueError:
            # raise Http404("No such page!")
            return  (paginator,'')
        except EmptyPage:
            return (paginator, '')

    # def count(self):
    #
    #     if  'page' not  in self.request.GET     :
    #         self.results.filter(li_name = self.request.GET['search_kinds'])
    #         return   '数据库总共大约有%s条搜索结果'   % len(self.results)
    #     elif  str(self.request.GET['page']) == '1':
    #         self.results.filter(li_name=self.request.GET['search_kinds'])
    #         return   '数据库总共大约有%s条搜索结果'   % len(self.results)

    def create_response(self):
        '''
        //
        '''
        # self.results=self.SearchQuerySet(object)
        self.context = {}
        self.context['query'] = self.get_query()
        # print self.request.GET('query')
        fd = field
        # exc = excel
        '''排序表头'''
        all_fields = fd.objects.values('field_name', 'field_val').distinct().order_by('add_date')
        self.context['search_option'] = []
        for obj in all_fields:

            self.context['search_option'].append(
                {'name': dict(obj)[u'field_name'], 'remark_name': dict(obj)[u"field_val"]})
        if 'search_kinds' in self.request.GET:
            # self.context['first_result_count'] = self.count()
            self.context['fileds_na'] = fd.objects.values('field_name')
            self.context['seach_k'] = self.request.GET['search_kinds']
            '''
            name标签
            '''
            # self.results = self.SearchQuerySet(object)
            # print   '下拉框框里面内容: %s' % self.request.GET['search_kinds']
            if self.request.GET['search_kinds'] != 'all':
                '''
                    分页功能
                '''
                self.results = self.results.filter(li_name=self.request.GET['search_kinds'])



                '''results排序下'''



                if 'page' not in self.request.GET:
                    # print  type(self.results)
                    # print    'sec_count : %s' % self.results.count()
                    self.context['first_result_count'] = '总共大约有%s条搜索结果' % (self.results.count())
                elif str(self.request.GET['page']) == '1':
                    # print  type(self.results)
                    self.context['first_result_count'] = '总共大约有%s条搜索结果' % (self.results.count())
                try:
                    self.results_per_page = self.results.count() + 1
                    pagenator, self.context['page'] = self.build_page()
                # except ValueError:
                #     self.context['page'] = ''
                except Exception as e:
                    # print  '异常:%s' %e
                    # print  'query:%s' %  self.context['query']
                    self.context['page'] = ''
                if self.context['page'] == '':
                    self.context['first_result_count'] = u'亲，页面不存在或者再刷新试试!'
            else:

                if 'page' not in self.request.GET:
                    # print  type(self.results)
                    self.context['first_result_count'] = '总共大约有%s条搜索结果' % (self.results.count())
                elif str(self.request.GET['page']) == '1':
                    # print  type(self.results)
                    self.context['first_result_count'] = '总共大约有%s条搜索结果' % (self.results.count())
                try:
                    self.results_per_page = self.results.count() + 1
                    pagenator,self.context['page'] = self.build_page()
                # except ValueError:
                #     self.context['page'] = ''
                except Exception as e:
                    # print  '异常:%s' % e
                    # print  'query:%s' % self.context['query']
                    self.context['page'] = ''
                if  self.context['page'] == '' :
                    self.context['first_result_count'] = u'亲，页面不存在或者再刷新试试!'
            # print '搜索框里面内容: %s' % self.context['query']

        '''
        过滤掉列数不一致的数据,事实证明是有用的

        '''
        # js = ''
        #
        # listx = ['COI', 'COI-2', 'COIII', '12S', '16S', '18S', '28S', 'H3', 'WNT', 'L494',
        #          'L168', 'ND1', 'Actin5c', '12-16S', 'EF1a', 'AK', 'GAPDH', 'Nak', 'PEPCK',
        #          'PDI', 'HSP', '转录组', '张鹏']
        '''js写死比较好'''
        # meta_list = ['li', 'dl',
        #              'dt', 'dd',
        #              'p', 'ul',
        #              'ol', 'label',
        #              'datalist', 'option',
        #              'summary', 'select',
        #              'optgroup', 'textarea',
        #              'video', 'source',
        #              'caption', 'metacharset',
        #              'meta', 'b',
        #              'marquee', 'pre',
        #              'title', 'dir',
        #              'menu', 'code',
        #              'small', 'big',
        #              ]
        # for  ii  in listx:
        #     js +=  '$("#%s").click(function(){$("%s :checkbox").attr("checked", true);});$("#rest_%s").click(function(){$("%s :checkbox").attr("checked", false);});'%(ii,meta_list[listx.index(ii)],ii,meta_list[listx.index(ii)])
        #
        # self.context['js_css']  = js
        return render(self.request, self.template, self.context)
        # pass









'''
select distinct 查询字段名   from 表名;
'''
