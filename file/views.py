# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse,HttpResponse
from  django.conf import  settings
import  os
# Create your views here.

'''只能在这边把函数写在这边了，无法引用别的app'''


def readFile(filename, chunk_size=512):
    # print filename
    fpath = os.path.join(settings.BASE_DIR, 'all_files', filename)
    if os.path.exists(fpath):
        print fpath
        with open(fpath, 'rb') as f:
            print settings.BASE_DIR
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


@csrf_exempt
def download_file(request, fn):
    the_file_name = fn # 显示在弹出对话框中的默认的下载文件名
    filename = fn # 要下载的文件路径
    # print  fn
    # print filename
    try:
        response = StreamingHttpResponse(readFile(filename))
    except :
        response = None
    # response['Content-File'] = fn
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    fpath = os.path.join(settings.BASE_DIR, 'all_files', filename)
    print fpath
    if os.path.exists(fpath):
        return response
    else:
        return  HttpResponse(u'不好意思，您想下载的文件不存在')
