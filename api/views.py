# -*- coding:utf-8 -*-
from django.db.models import Count, Sum
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.db.transaction import commit_on_success
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

from articles.models import Article, Word
from media.models import Medium
from journalists.models import Journalist
from tools.pyictclas import PyICTCLAS, CodeType, POSMap

import requests
import json
import time
import urllib
import re
import datetime
from dateutil.relativedelta import relativedelta

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
        INTERFACES = { i : i + '()' for i in ['detail', 'monthly_keywords', 'edit', 'resort', 'word'] }

        def monthly_keywords():
            data = {}
            data['timeline'] = {"type":"default","startDate":"2012",}
            data['timeline']['date'] = []

            originated_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
            medium_id = 951#int(request.GET.get('medium_id'))
            for i in range(12):
                start_date  = originated_date + relativedelta(months=+i)
                end_date    = originated_date + relativedelta(months=+i+1)
                article_id_list    = Article.objects.filter(medium_id=medium_id).filter(publication_date__gt=start_date).filter(publication_date__lt=end_date).values_list('id', flat=True)
                words       = Word.objects.filter(article_id__in=article_id_list).values('word', 'frequency').order_by('-frequency')

                _d = {}
                for word in words:
                    if word['word'] in _d:
                        _d[word['word']] += word['frequency']
                    else:
                        _d[word['word']] = word['frequency']
                _d = sorted(_d.iteritems(), key=lambda (k, v): (v,k))

                monthly_chart_data = unicode([list(e) for e in _d[::-1][:15]]).replace('L', '').replace('[u', '[')
                data['timeline']['date'].append({
                    'startDate' : start_date.strftime('%Y,%m'),
                    'headline' : 'Frequent word on %s' % start_date.strftime('%B'),
                    'text': '<div id="id_chart_'+str(i)+'" style="width:700px; height:260px;margin-right:30px;"></div>' + 
                            '<script>$.jqplot("id_chart_'+str(i)+'", ['+monthly_chart_data+'], {seriesDefaults:{renderer:$.jqplot.BarRenderer,rendererOptions: {varyBarColor: true}},axes:{xaxis:{renderer: $.jqplot.CategoryAxisRenderer}}}); XINZHUAN.words['+str(i+1)+'] = '+monthly_chart_data+';</script>'
                })
                # break


            return HttpResponse(json.dumps(data))


        def word():
            word = request.REQUEST.get('word')
            originated_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
            medium_id = 951#int(request.GET.get('medium_id'))
            word_frequency_sum_list = []
            month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            for i in range(12):

                start_date  = originated_date + relativedelta(months=+i)
                end_date    = originated_date + relativedelta(months=+i+1)

                word_frequency_sum = Word.objects.filter(word=word).aggregate(sum=Sum('frequency'))['sum'] or 0
  

                word_frequency_sum_list.append(['%s 1' % month_list[i], word_frequency_sum])
                
            return self._response(word_frequency_sum_list)

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
        INTERFACES = { i : i + '()' for i in ['ictclas', 'translation', 'check', 'resort', 'delete'] }

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
            content = request.POST.get('content').encode('utf-8')
            show_pinyin = int(request.POST.get('show_pinyin', 1))
            r = requests.get('http://translate.google.cn/translate_a/t?client=t&text='+urllib.quote(content)+'&hl=zh-CN&sl=zh-CN&tl=en&ie=UTF-8&oe=UTF-8&multires=1&prev=btn&ssel=0&tsel=0&sc=1')
            post_translational_and_pinyin = re.search('\[\[\["(.*)]],,"zh-CN"', r.content).groups()[0].split('","')
            response = {}
            response['result'] = post_translational_and_pinyin[0]
            if show_pinyin:
                response['pinyin'] = post_translational_and_pinyin[-1][0:-1]
            #re.search('^\[\[\["(.*)"]],,"zh-CN"', s); print r.groups()[0]
            return self._response(response)

        def check():
            domain = get_current_site(request).domain
            content = request.POST.get('content').encode('utf-8')
            r = requests.post('http://%s/api/tools/ictclas.json' % domain, {'content': content, 'frequency_limit' : 1})
            word_list = r.json()['response']['result'].split(' ')
            dubious_word_index_list = []
            for i in range(len(word_list)):
                ######检查助词######
                word = word_list[i]
                if len(word) > 0 and word[-1] == 'u' and word[:-2] in ['的', '地']:
                    if word[:-2] == '的' and word_list[(i+1)][-1] != 'n' \
                        or word[:-2] == '地' and word_list[(i+1)][-1] not in ['v',]:
                        word_list[i] = '{' + word_list[i][:-2] + '}'
                    else:
                        word_list[i] = word_list[i][:-2]
                else:
                    word_list[i] = word_list[i][:-2]
            response = {
                'result' : '.'.join(word_list),
                'error' : len(dubious_word_index_list),
            }
            return self._response(response)

        return eval(INTERFACES[interface])