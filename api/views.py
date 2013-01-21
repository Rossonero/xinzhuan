# -*- coding:utf-8 -*-
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.transaction import commit_on_success
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

from media.models import Medium
from journalists.models import Journalist

import requests
import json
import time

@commit_on_success
@csrf_exempt
def route(request, app_name, interface):
    try:
        f = getattr(Apis(), app_name)
    except:
        return HttpResponse(json.dumps({'code': 500, 'errorMessage': '没有找到指定接口'}))
    return f(request, interface)

class Apis():
    def _date_handler(self, obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def _content_handler(self, content, summary=True):
        soup = BeautifulSoup(content)
        v = ''.join(soup.findAll(text=True))
        v = v.replace('&nbsp;', '')
        if summary:
            return v[:100]
        else:
            return v

    def _error(self, code=51, extra_message=''):
        error_dict = {}
        #weixin interface
        error_dict[21] = '请求数据不合法'

        error_dict[51] = '根据ID找不到对应的Object'
        error_dict[52] = '缺少需要的参数'
        error_dict[53] = 'response不是dict'

        error_dict[71] = '已经邀请过了'
        error_dict[72] = '已经申请过了'
        return HttpResponse(json.dumps({'code': code, 'errorMessage': error_dict[code] + extra_message}))


    def _response(self, data = {}, format='json'):
        '''
        type(data) == __dict__
        '''
        return HttpResponse(json.dumps({'code': 0, 'response': data }, default=self._date_handler))

    @commit_on_success
    @csrf_exempt
    def media(self, request, interface):
        INTERFACES = { i : i + '()' for i in ['list', 'add', 'edit', 'resort', 'delete'] }

        def list():
            page = int(request.REQUEST.get('page', 1))
            result = Medium.objects.all().order_by('name')[(page-1)*30:page*30]
            ms = []
            for medium in result:
                print medium.language
                ms.append({
                    'name' : medium.name,
                    'language' : medium.language or 'zh',
                    'category' : medium.get_category_display(),
                    'reports' : {
                        'counter' : Journalist.objects.filter(medium=medium).count()
                    }
                })

            return self._response(ms)

        return eval(INTERFACES[interface])

