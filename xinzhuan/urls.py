from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'xinzhuan.views.newspapers'),
    url(r'^api/', include('api.urls')),
    url(r'^data-and-tools/', include('tools.urls')),
    url(r'^provincial-media-data/(?P<province>.*?)/?$', 'xinzhuan.views.statistic', name='statistic'),
    url(r'^newspapers/$', 'xinzhuan.views.newspapers', name='newspapers'),
    url(r'^newspapers/(?P<medium_id>\d+)/$', 'xinzhuan.views.analysis'),
    url(r'^analysis/', 'xinzhuan.views.analysis', name='analysis'),
    url(r'^handler/', 'xinzhuan.views.handler'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
