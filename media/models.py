# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from misc.models import Area

LANGUAGE_CHOICE = (
    ('zh', 'Chinese'),
    ('en', 'English'),
    ('ru', 'Russian'),
    ('sjo', 'Xibe'),
    ('za', 'Zhuang'),
    ('kk', 'Kazakh'),
    ('ug', 'Uyghur'),
    ('ko', 'Korean'),
    ('bo', 'Tibetan'),
    ('mn', 'Mongolian'),
)
MEDIUM_CATEGORY = (
    ('newspaper','Newspaper'),
    ('periodical','Periodical'),
    ('radio_and_tv','Radio and Tv'),
)

class Medium(models.Model):
    name           = models.CharField(max_length=128)
    address        = models.TextField(blank=True)
    category       = models.CharField(max_length=64, choices=MEDIUM_CATEGORY)
    cn             = models.CharField(max_length=64, blank=True, null=True)
    code           = models.CharField(max_length=64, blank=True, null=True)
    language       = models.CharField(max_length=16, choices=LANGUAGE_CHOICE, blank=True)
    phone          = models.CharField(max_length=32, blank=True, null=True)
    sponsor        = models.ForeignKey('Unit', related_name='sponsor', blank=True)
    competent_dept = models.ForeignKey('Unit', related_name='competent_dept', blank=True)
    region         = models.ForeignKey(Area, blank=True, null=True)
    def __unicode__(self):
        return self.name


class Unit(models.Model):
    name   = models.CharField(max_length=128)
    region = models.ForeignKey(Area, blank=True, null=True)

    def __unicode__(self):
        return self.name