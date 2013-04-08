# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from media.models import Medium
from journalists.models import Journalist

import requests

class Article(models.Model):
    title            = models.CharField(max_length=128)
    content          = models.TextField()
    issue            = models.IntegerField()
    page             = models.CharField(max_length=64)
    publication_date = models.DateField()
    medium           = models.ForeignKey(Medium)
    url              = models.URLField(blank=True)
    author           = models.ForeignKey(Journalist, blank=True, null=True)
    author_name      = models.CharField(max_length=64, blank=True)

    def get_word_frequency(self):
        r = requests.post('http://127.0.0.1:8000/api/tools/jieba.json', {'content': self.content})
        return r.json()['response']['word_frequency']

    def save_word_frequency(self):
        for e in self.get_word_frequency():
            word, flag = e[0].split('/')
            try:
                if e[-1] > 2 and len(word) >= 2:
                    new_word, created = Word.objects.get_or_create(word=word, category=flag, article=self, publication_date=self.publication_date, medium=self.medium, frequency=e[-1])
            except:
                print self.title


WORD_CATEGORY_CHOICE = (
    ('n', 'noun'),
    ('v', 'verb'),
    ('a', 'adjective'),
    ('d', 'adverb'),
)
class Word(models.Model):
    word             = models.CharField(max_length=16)
    category         = models.CharField(max_length=8) #, choices=WORD_CATEGORY_CHOICE
    article          = models.ForeignKey(Article)
    medium           = models.ForeignKey(Medium)
    publication_date = models.DateField()
    frequency        = models.IntegerField()

class HotWord(models.Model):
    word             = models.CharField(max_length=16)
    english          = models.CharField(max_length=64, blank=True)
    monthly_frequency= models.IntegerField()
    month            = models.IntegerField()
    medium           = models.ForeignKey(Medium)

# class ErrorWord(models.Model):
#     wrong_word             = models.CharField(max_length=16)
#     right_word             = models.CharField(max_length=16)

# class Photo(models.Model):
#     article          = models.ForeignKey(Article)
#     summary          = models.TextField(blank=True)
#     image            = models.ImageField()