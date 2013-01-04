# -*- coding: utf-8 -*-
from django.db import models

class Area(models.Model):
    name      = models.CharField(max_length=64)
    area_id   = models.CharField(max_length=32)
    parent_id = models.CharField(max_length=32)