# -*- coding: utf-8 -*-
from django.db import models

from media.models import Medium

class Journalist(models.Model):
    name      = models.CharField(max_length=64)
    medium = models.ForeignKey(Medium)

    def newspaper_name(self):
    	return self.medium.name