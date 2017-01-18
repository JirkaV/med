from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sample_matching/$', views.match_dna_sample, name='match_dna_sample'),
    url(r'^sample_matching/print/', views.dna_comparison_for_print,
                                    name='dna_comparison_for_print'),

    url(r'sequencer/$', views.sequencer, name='sequencer'),
    url(r'sequencer/select-reference/$', views.sequencer_select_reference,
                                         name='sequencer_select_reference'),
    url(r'sequencer/input-reference/$', views.sequencer_input_reference,
                                         name='sequencer_input_reference'),
    url(r'sequencer/sample/add/$', views.add_to_sequencer, name='add_to_sequencer'),
    url(r'sequencer/sample/delete/(?P<sample_id>\d+)/$', views.sequencer_delete_sample,
                                                         name='sequencer_delete_sample'),
    url(r'sequencer/reset/$', views.reset_sequencer, name='reset_sequencer'),
    url(r'sequencer/result/print/$', views.sequencer_result_for_print,
                                     name='sequencer_result_for_print'),
]
