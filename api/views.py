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

from articles.models import Article
from media.models import Medium
from journalists.models import Journalist
from tools.pyictclas import PyICTCLAS, CodeType, POSMap

import requests
import json
import time
import urllib
import re

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

    def articles(self, request, interface):
        INTERFACES = { i : i + '()' for i in ['detail', 'add', 'edit', 'resort', 'delete'] }

        def detail():
            article_id = int(request.REQUEST.get('article_id'))
            article = Article.objects.get(pk=article_id)

            return self._response(model_to_dict(article))
        return eval(INTERFACES[interface])


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

    def tools(self, request, interface):
        INTERFACES = { i : i + '()' for i in ['ictclas', 'translation', 'edit', 'resort', 'delete'] }

        def ictclas():
            ictclas = PyICTCLAS()
            ictclas.ictclas_init()
            ictclas.ictclas_setPOSmap(POSMap.ICT_POS_MAP_SECOND)
            content = request.POST.get('content')
            word_frequency_limit = int(request.POST.get('frequency_limit', 1))
            response = {
                'result' : ictclas.ictclas_paragraphProcess(content, CodeType.CODE_TYPE_UTF8).value.lstrip()
            }
            word_array = []
            word_frequency = {}
            allow_parts_of_speech = ['n', 'v', 'a']
            ignore_speech  = ['是/v', '有/v', '-/n']
            for word in response['result'].split(' '):
                if len(word) > 0 and word[-1] in allow_parts_of_speech and word not in ignore_speech: word_array.append(word)
            for word in set(word_array):
                if word_array.count(word) >= word_frequency_limit: word_frequency[word] = word_array.count(word)

            sorted_word_frequency = sorted(word_frequency.iteritems(), key=lambda (k, v) : (v,k))
            response['word_frequency'] = list(reversed(sorted_word_frequency))
            return self._response(response)

        def translation():
            # text = request.POST.get('text').encode('utf-8')
            text = '中国报纸分析'.encode('utf-8')
            show_pinyin = int(request.POST.get('show_pinyin', 1))
            r = requests.get('http://translate.google.cn/translate_a/t?client=t&text='+urllib.quote(text)+'&hl=zh-CN&sl=zh-CN&tl=en&ie=UTF-8&oe=UTF-8&multires=1&prev=btn&ssel=0&tsel=0&sc=1')
            post_translational_and_pinyin = re.search('\[\[\["(.*)]],,"zh-CN"', r.content).groups()[0].split('","')
            response = {}
            response['result'] = post_translational_and_pinyin[0]
            if show_pinyin:
                response['pinyin'] = post_translational_and_pinyin[-1][0:-1]
            #re.search('^\[\[\["(.*)"]],,"zh-CN"', s); print r.groups()[0]
            return self._response(response)


        return eval(INTERFACES[interface])