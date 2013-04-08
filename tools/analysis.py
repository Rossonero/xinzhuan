# -*- coding: utf-8 -*-
import sys
import requests
import datetime
from dateutil.relativedelta import relativedelta

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



if __name__ == '__main__':
    generate_monthly_keywords(1836)