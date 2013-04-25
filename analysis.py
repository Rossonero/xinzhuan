# -*- coding: utf-8 -*-
import sys
import requests
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
sys.path.append('/home/perchouli/workspaces/xinzhuan')

from articles.models import Article, Word, HotWord

def generate_monthly_keywords(medium_id):
    originated_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
    monthly_chart_data = []
    for i in range(12):
        start_date  = originated_date + relativedelta(months=+i)
        end_date    = originated_date + relativedelta(months=+i+1)
        words       = Word.objects.filter(medium_id=medium_id).filter(publication_date__gt=start_date).filter(publication_date__lt=end_date).exclude(category='m')

        _d = {}
        for word in words:
            if word.word in _d:
                _d[word.word] += int(word.frequency)
            else:
                _d[word.word] = int(word.frequency)
        _d = sorted(_d.iteritems(), key=lambda (k, v): (v,k))
        for e in _d[::-1][:15]:
            hot_word = HotWord()
            hot_word.month = i+1
            hot_word.word = e[0]
            hot_word.monthly_frequency = e[1]
            hot_word.medium_id = medium_id
            hot_word.save()

def get_data(hot_word):
    # word = request.REQUEST.get('word')
    originated_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
    medium_id = hot_word.medium_id
    word_frequency_sum_list = []
    month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    for i in range(12):
        print hot_word.word
        start_date  = originated_date + relativedelta(months=+i)
        end_date    = originated_date + relativedelta(months=+i+1)
        word_frequency_sum = Word.objects.filter(word=hot_word.word).filter(medium_id=medium_id).filter(publication_date__gt=start_date).filter(publication_date__lt=end_date).aggregate(sum=Sum('frequency'))['sum'] or 0

        word_frequency_sum_list.append(['%s 1' % month_list[i], word_frequency_sum])

    data = word_frequency_sum_list
    return data


def filter_word(medium_id):
    hot_word = HotWord.objects.filter(medium_id=medium_id).values_list('pk', flat=True)
    print hot_word
    # words = Word.objects.filter

def trans():
    all_hot_word = HotWord.objects.filter(medium_id=1399).values_list('word', flat=True)

    d = []
    for w in list(set(all_hot_word)):
        if w in d:
            continue

        r = requests.post('http://127.0.0.1:8000/api/tools/translation.json', {'content' : w})
        try:
            e = r.json()['response']['result']
        except:
            print w
        hot_word = HotWord.objects.filter(word=w).update(english=e)
        d.append(w)


if __name__ == '__main__':
    # generate_monthly_keywords(1399)
    d = []
    for hot_word in HotWord.objects.filter(medium_id=1399):
        if hot_word.word in d:
            continue
        d.append(hot_word.word)
        data = get_data(hot_word)
        hot_word.data = data
        hot_word.save()
    # for w in [{"word": "南方周末","data": ""}, {"word": "为什么","data": ""}, {"word": "负责人","data": ""}, {"word": "工作人员","data": ""}, {"word": "俄罗斯","data": ""}, {"word": "越来越","data": ""}, {"word": "方舟子","data": ""}, {"word": "菲律宾","data": ""}, {"word": "开发商","data": ""}, {"word": "钓鱼岛","data": ""}, {"word": "航天员","data": ""}, {"word": "奥巴马","data": ""}, {"word": "委员会","data": ""}, {"word": "奥运会","data": ""}, {"word": "温州市","data": ""}, {"word": "罗姆尼","data": ""}, {"word": "候选人","data": ""}, {"word": "民主党","data": ""}, {"word": "飞行员","data": ""}, {"word": "十八大","data": ""}]:
    #     hot_word = HotWord.objects.filter(medium_id=1836).filter(word=w['word'])[0]
    #     data = get_data(hot_word)
    #     hot_word.data = data
    #     hot_word.save()
    # trans()