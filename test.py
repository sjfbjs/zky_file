#coding:utf-8
#from zky_file.settings import MEDIA_ROOT
import os
MEDIA_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'all_files')
print MEDIA_ROOT
#from  index.models import *
import sys,xlrd
reload(sys)
sys.setdefaultencoding('utf-8')
#f = file
#print f.objects.all()
import MySQLdb
#db = MySQLdb.connect('127.0.0.1','root','','zky', charset="utf8")
db = MySQLdb.connect('127.0.0.1','root','','zky')
cur=db.cursor()
#cur.execute('select * from  index_file where up_status="2";')
cur.execute("SET NAMES utf8;")
cur.execute('select filename from  index_file ;')
objs=cur.fetchall()
#print objs
if objs:
	for obj in objs:
		#print obj[0]
		if obj[0]:
			fn = obj[0]
			#cur.execute('update index_file set up_status='2' where filename=%s'%fn)
			print fn
			fname, ext = fn.split('.')
			fpath = os.path.join(MEDIA_ROOT, fn)
			print fpath
			workbook = xlrd.open_workbook(str(fpath))
			if len(workbook.sheet_names()) > 0:
				sheet_name = workbook.sheet_names()[0]
				print sheet_name
				sheet = workbook.sheet_by_name(sheet_name)
				# sheet的名称，行数，列数           
				print sheet.name, sheet.nrows, sheet.ncols
				
			#print fname
			#print ext

db.close()
