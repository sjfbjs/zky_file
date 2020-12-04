#coding:utf-8
from  django.forms import forms,ModelForm
import  models
class IndexModelForm(ModelForm):
    class Meta:
        model = models.excel
        exclude=()