# -*- coding:utf-8 -*-
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from media.models import Medium, Unit
from misc.models import Area
from articles.models import Article

from dateutil.relativedelta import relativedelta
import datetime

def home(request):
    ctx = {
        'lang' : _('Chinese')
    }
    return TemplateResponse(request, 'home.html', ctx)

def statistic(request, province):
    category = request.GET.get('category')
    if not province:
        media = category and Medium.objects.filter(category=category).order_by('name') or Medium.objects.all().order_by('name')
        region = Area.objects.get(pk=3356)

        media_count = Medium.objects.all().values('id')
    else:
        province = province.capitalize()
        region = get_object_or_404(Area, en=province)
        media = category and Medium.objects.filter(region=region).filter(category=category).order_by('name') or Medium.objects.filter(region=region).order_by('name')

        media_count = Medium.objects.filter(region=region).values('id')

    counters = {
        'newspaper' : media_count.filter(category='newspaper').count(),
        'radio_and_tv' : media_count.filter(category='radio_and_tv').count(),
        'periodical' : media_count.filter(category='periodical').count()
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


def analysis(request, medium_id):
    medium = get_object_or_404(Medium, pk=medium_id)

    ctx = {
        'medium' : medium,
        'title' : medium.english_name,
    }
    return TemplateResponse(request, 'analysis.html', ctx)

def newspapers(request):
    
    ctx = {
        'newspapers' : Medium.objects.filter(english_name__isnull=False).order_by('name')
    }
    return TemplateResponse(request, 'newspapers.html', ctx)


def handler(request):
    articles = Article.objects.all()
    # 分页
    paginator = Paginator(articles, 100)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1    
    articles = paginator.page(page)
    ctx = {
        'articles' : articles
    }
    return TemplateResponse(request, 'handler.html', ctx)