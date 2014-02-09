from django.conf.urls import *

urlpatterns = patterns('med.glukokortikoidy.views',
    url(r'^$', 'calculator', name='glukokortikoidy_calculator'),
)
