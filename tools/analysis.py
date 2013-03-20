# -*- coding: utf-8 -*-
import sys
import requests

sys.path.append('/home/perchouli/workspaces/xinzhuan')

from articles.models import Article, Word

if __name__ == '__main__':
    articles = Article.objects.filter(medium_id=951).exclude(page=u'文化')
    for a in articles:
        r = requests.post('http://127.0.0.1:8000/api/tools/ictclas.json', {'content' : a.content})
        print r.json['response']['word_frequency']
        break