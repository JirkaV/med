from django.conf import settings
from django.conf.urls import *
from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^dna/', include('med.dna.urls')),
    url(r'^glukokortikoidy/', include('med.glukokortikoidy.urls')),
    url(r'^cmv/', include('med.cmv.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
    )
