from django.conf.urls import patterns, include, url

urlpatterns = patterns('pairwork.background.views',
    url(r'^/$', 'BHome', name='FHome'),
)