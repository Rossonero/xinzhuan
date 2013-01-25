# -*- coding:utf-8 -*-
from django.template.response import TemplateResponse


def ictclas(request):
	ctx = {

	}
	return TemplateResponse(request, 'tools/ictclas.html', ctx)