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
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1    
    media = paginator.page(page)
    
    if page <= 10:
        start_page= False
        end_page = paginator.num_pages > 20 and True or False
        page_range = paginator.page_range[0:20]
    elif page > 10 and page < paginator.num_pages - 10:
        start_page,end_page = True, True
        page_range = paginator.page_range[page-9:page+10]
    else:
        start_page,end_page = True, False
        page_range = paginator.page_range[page-9:page+10]

    ctx = {
        'paginator' : paginator,
        'page_range' : page_range,
        'start_page' : start_page,
        'end_page' : end_page,
        'region' : region,
        'counters' : counters,
        'media' : media,
        'provinces' : Area.objects.filter(parent_id=0).exclude(pk__gt=3352)
    }
    return TemplateResponse(request, 'statistic.html', ctx)


def analysis(request):
    sw = Medium.objects.get(pk=1081)
    pd = Medium.objects.get(pk=951)
    ctx = {

    }
    return TemplateResponse(request, 'analysis.html', ctx)