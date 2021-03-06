from django.shortcuts import render
from django.template.defaultfilters import date as template_date
from django.utils.timezone import now
from common.utils import absolute_redirect
from .forms import (DNASampleForm, PlainDNASampleForm,
                    ReferenceSelectForm, ReferenceInputForm)
from .utils import (get_best_offset, get_triplets,
                    prepare_output_rows, get_output_rows,
                    calculate_statistics)

def match_dna_sample(request):
    if request.method == 'POST':
        form = DNASampleForm(request.POST)
        if form.is_valid():
            dna_sample = form.cleaned_data['dna_sample']
            reference_dna_model = form.cleaned_data['reference_dna']
            ref_dna = reference_dna_model.dna
            ref_name = reference_dna_model.name
            dna_sample = dna_sample.strip('\r\n').upper()
            best_offset = get_best_offset(ref_dna, dna_sample)
            changes = get_triplets(ref_dna, dna_sample, best_offset,
                                   different_only=True)
            # save data to session for print
            request.session['timestamp'] = template_date(now(), 'r')  # Django does not like timestamps in session anymore
            request.session['best_offset'] = best_offset
            request.session['reference_dna'] = ref_dna
            request.session['reference_name'] = ref_name
            request.session['changes'] = changes
            request.session['dna_sample'] = dna_sample

            return render(request,
                          'dna/dna_matching_result.html',
                          {'reference_name': ref_name,'changes': changes})
    else:
        form = DNASampleForm()
    return render(request, 'dna/dna_sample_form.html', {'form': form})

def dna_comparison_for_print(request):
    try:
        # pick up data from session
        timestamp = request.session['timestamp']
        best_offset = request.session['best_offset']
        reference_dna = request.session['reference_dna']
        reference_name = request.session['reference_name']
        changes = request.session['changes']
        dna_sample = request.session['dna_sample']
    except KeyError:
        return render(request, 'dna/dna_matching_result_for_print.html',
                              {'session_error': True})
    rows = get_output_rows(prepare_output_rows(reference_dna,
                                               [{'dna': dna_sample,
                                                 'offset': best_offset}]),
                           add_index_numbers=True)
    return render(request, 'dna/dna_matching_result_for_print.html',
                           {'reference_name': reference_name,
                            'changes': changes,
                            'rows': rows,
                            'timestamp_string': timestamp})

def sequencer(request):
    '''show main sequencer page'''
    return render(request, 'dna/sequencer.html',
                  {'reference': request.session.get('sequencer_reference', ''),
                   'reference_name': request.session.get('sequencer_reference_name', ''),
                   'samples': request.session.get('samples_data', [])})

def reset_sequencer(request):
    '''reset sequencer data'''
    if request.method != 'POST':
        return absolute_redirect('sequencer')
    request.session['sequencer_reference'] = ''
    request.session['samples_data'] = []
    return absolute_redirect('sequencer')

def sequencer_select_reference(request):
    '''view for picking an existing reference from the database'''
    if request.method == 'POST':
        form = ReferenceSelectForm(request.POST)
        if form.is_valid():
            request.session['sequencer_reference'] = form.cleaned_data['reference_dna'].dna
            request.session['sequencer_reference_name'] = form.cleaned_data['reference_dna'].name
            return absolute_redirect('sequencer')
    else:
        form = ReferenceSelectForm()

    return render(request, 'dna/sequencer_reference_select_form.html', {'form': form})

def sequencer_input_reference(request):
    '''view for manual reference input (one-off use, won't be remembered)'''
    if request.method == 'POST':
        form = ReferenceInputForm(request.POST)
        if form.is_valid():
            request.session['sequencer_reference'] = form.cleaned_data['reference_dna_string']
            request.session['sequencer_reference_name'] = form.cleaned_data['reference_dna_name']
            return absolute_redirect('sequencer')
    else:
        form = ReferenceInputForm()

    return render(request, 'dna/sequencer_reference_input_form.html', {'form': form})


def add_to_sequencer(request):
    '''add new data to sequencer'''
    # safety check first
    if not request.session.get('sequencer_reference', ''):
        return absolute_redirect('sequencer')
    reference_length = len(request.session['sequencer_reference'])

    if request.method == 'POST':
        form = PlainDNASampleForm(request.POST,
                                  reference_length=reference_length)
        if form.is_valid():
            dna_sample = form.cleaned_data['dna_sample']
            sample = {'dna': dna_sample,
                      'offset': get_best_offset(request.session['sequencer_reference'], dna_sample)}
            # appending directly to request.session['samples_data'] does not seem to work as expected
            try:
                tmp = request.session['samples_data']
            except KeyError:
                tmp = []
            tmp.append(sample)
            request.session['samples_data'] = tmp
            return absolute_redirect('sequencer')
    else:
        form = PlainDNASampleForm(reference_length=reference_length)

    return render(request, 'dna/sequencer_dna_sample_form.html', {'form': form})

def sequencer_result_for_print(request):
    '''show the sequencer result page'''
    if not (request.session.get('sequencer_reference', '')
            and request.session.get('samples_data', [])):
        return absolute_redirect('sequencer')

    rows = prepare_output_rows(request.session['sequencer_reference'],
                               request.session['samples_data'])
# FIXME    differences_cnt = calculate_total_differences(rows)

    # per user request - calculate statistics only if there is exactly
    # one sample, base it on the sample length only
    if len(request.session['samples_data']) == 1:
        show_statistics = True
        sample = request.session['samples_data'][0]
        s_offset = sample['offset']
        s_length = len(sample['dna'])
        # rows[2] is the one with SAME_CHAR, DIFF_CHAR etc.
        differences_cnt, similarity_ratio = calculate_statistics(rows[2][s_offset:s_offset+s_length])
    else:
        differences_cnt = 0
        similarity_ratio = 0.0
        show_statistics = False

    final_output_rows = get_output_rows(rows,
                                        add_index_numbers=True,
                                        separator_line=True)

    return render(request, 'dna/sequencer_result.html',
                           {'reference_name': request.session['sequencer_reference_name'],
                            'rows': final_output_rows,
                            'differences_cnt': differences_cnt,
                            'similarity_ratio': similarity_ratio,
                            'show_statistics': show_statistics,
                            'timestamp_string': template_date(now(), 'r')})

def sequencer_delete_sample(request, sample_id):
    '''deletes a specific sample from sequencer'''
    if request.method != 'POST':
        return absolute_redirect('sequencer')
    samples_data = request.session['samples_data']
    to_delete = int(sample_id)
    res = []
    for i, sample in enumerate(samples_data, start=1):
        if i == to_delete:
            continue  # delete this one
        res.append(sample)
    request.session['samples_data'] = res
    return absolute_redirect('sequencer')
