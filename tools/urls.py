from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tools.views',
    url(r'^$', 'ictclas'),
    url(r'^ictclas/', 'ictclas'),
)
