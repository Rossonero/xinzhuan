# -*- coding: utf-8 -*-
from django.db import models

class Area(models.Model):
    name      = models.CharField(max_length=64)
    en        = models.CharField(max_length=128)
    area_id   = models.CharField(max_length=32)
    parent_id = models.CharField(max_length=32)
    summary   = models.TextField(blank=True)