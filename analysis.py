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

if __name__ == '__main__':
    # d = []
    # for hot_word in HotWord.objects.filter(pk__gt=11):
    #     if hot_word.word in d:
    #         continue
    #     d.append(hot_word.word)
    #     data = get_data(hot_word)
    #     hot_word.data = data
    #     hot_word.save()
    for w in [{"word": "农民工","data": ""}, {"word": "进一步","data": ""}, {"word": "志愿者","data": ""}, {"word": "越来越","data": ""}, {"word": "幼儿园","data": ""}, {"word": "社会主义","data": ""}, {"word": "消费者","data": ""}, {"word": "负责人","data": ""}, {"word": "叙利亚","data": ""}, {"word": "俄罗斯","data": ""}, {"word": "大学生","data": ""}, {"word": "本报讯","data": ""}, {"word": "共青团","data": ""}, {"word": "青少年","data": ""}, {"word": "新华社","data": ""}, {"word": "中国青年报","data": ""}, {"word": "为什么","data": ""}, {"word": "全国政协","data": ""}, {"word": "人大代表","data": ""}, {"word": "学雷锋","data": ""}, {"word": "胡锦涛","data": ""}, {"word": "雷锋精神","data": ""}, {"word": "委员会","data": ""}, {"word": "工作人员","data": ""}, {"word": "年轻人","data": ""}, {"word": "有限公司","data": ""}, {"word": "总书记","data": ""}, {"word": "团组织","data": ""}, {"word": "航天员","data": ""}, {"word": "毕业生","data": ""}, {"word": "奥运会","data": ""}, {"word": "运动员","data": ""}, {"word": "钓鱼岛","data": ""}, {"word": "国务院","data": ""}, {"word": "十八大","data": ""}, {"word": "中国共产党","data": ""}, {"word": "发展观","data": ""}, {"word": "小康社会","data": ""}, {"word": "现代化","data": ""}, {"word": "互联网","data": ""}]:
        hot_word = HotWord.objects.filter(medium_id=1836).filter(word=w['word'])[0]
        data = get_data(hot_word)
        hot_word.data = data
        hot_word.save()