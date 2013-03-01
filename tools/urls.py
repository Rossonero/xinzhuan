from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tools.views',
    url(r'^(?P<route>.*?)/?$', 'handler'),

)
