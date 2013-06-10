from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('med.dna.views',
    url(r'^sample_matching/$', 'match_dna_sample', name='match_dna_sample'),
    url(r'^sample_matching/print/', 'dna_comparison_for_print',
                                    name='dna_comparison_for_print'),
)
