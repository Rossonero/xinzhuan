# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from media.models import Medium
from journalists.models import Journalist

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