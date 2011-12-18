from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^dna/', include('med.dna.urls')),
    url(r'^glukokortikoidy/', include('med.glukokortikoidy.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
