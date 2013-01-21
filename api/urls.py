from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'^(?P<app_name>.*)/(?P<interface>.*).json', 'route'),
)
