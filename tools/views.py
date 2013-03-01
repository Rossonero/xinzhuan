# -*- coding:utf-8 -*-
from django.template.response import TemplateResponse


def handler(request, route):
    if not route: route = 'ictclas'
    ctx = {
        'route' : route
    }
    title = {
        'ictclas' : 'ICTCLAS',
        'translation' : 'Chinese Translation',
        'data' : 'Data'
    }
    ctx['title'] = title[route]
    return TemplateResponse(request, 'tools/body.html', ctx)