# -*- coding:utf-8 -*-
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from media.models import Medium, Unit
from misc.models import Area

def home(request):
    ctx = {
        'lang' : _('Chinese')
    }
    return TemplateResponse(request, 'home.html', ctx)

def statistic(request, province):
    if not province:
        media = Medium.objects.all().order_by('name')
        region = Area.objects.get(pk=3356)
    else:
        province = province.capitalize()
        region = get_object_or_404(Area, en=province)
        media = Medium.objects.filter(region=region).order_by('name')

    counters = {
        'newspaper' : media.filter(category='newspaper').count(),
        'radio_and_tv' : media.filter(category='radio_and_tv').count(),
        'periodical' : media.filter(category='periodical').count()
    }

    # 分页
    paginator = Paginator(media, 30)
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1    
    media = paginator.page(page)

    ctx = {
        'region' : region,
        'counters' : counters,
        'media' : media,
        'provinces' : Area.objects.filter(parent_id=0).exclude(pk__gt=3352)
    }
    return TemplateResponse(request, 'statistic.html', ctx)