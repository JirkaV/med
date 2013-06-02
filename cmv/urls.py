from django.conf.urls import patterns, url

urlpatterns = patterns('cmv.views',
    url(r'^$', 'prehled', name='cmv_prehled'),
    url(r'^upload/$', 'upload', name='cmv_upload'),
)
