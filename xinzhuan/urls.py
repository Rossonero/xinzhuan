from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^api/', include('api.urls')),
    url(r'^$', 'xinzhuan.views.home'),
    # TODO: FIX IT
    # url(r'^provincial-media-data/', 'xinzhuan.views.statistic'),
    url(r'^provincial-media-data/(?P<province>.*?)/?$', 'xinzhuan.views.statistic', name='statistic'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
