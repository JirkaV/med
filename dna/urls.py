from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sample_matching/$', views.match_dna_sample, name='match_dna_sample'),
    url(r'^sample_matching/print/', views.dna_comparison_for_print,
                                    name='dna_comparison_for_print'),
]
