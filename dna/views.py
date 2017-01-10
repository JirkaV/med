from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import date as template_date
from django.utils.timezone import now
from .models import ReferenceDNA
from .forms import DNASampleForm, PlainDNASampleForm, ReferenceSelectForm
from .utils import get_best_offset, get_triplets, align_samples
from .utils import get_output_rows, prepare_sample_for_display
from .utils import prepare_sequencer_data_for_display

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
    rows = get_output_rows(prepare_sample_for_display(reference_dna,
                                                      dna_sample, best_offset),
                           add_index_numbers=True)
    return render(request, 'dna/dna_matching_result_for_print.html',
                           {'reference_name': reference_name,
                            'changes': changes,
                            'rows': rows,
                            'timestamp_string': timestamp})

def sequencer(request):
    '''show main sequencer page'''
    return render(request, 'dna/sequencer.html',
                  {'reference_DNA': request.session.get('sequencer_reference', ''),
                   'samples': request.session.get('samples_data', [])})

def reset_sequencer(request):
    '''reset sequencer data'''
    request.session['sequencer_reference'] = ''
    request.session['samples_data'] = []
    return redirect('sequencer')

def sequencer_select_reference(request):
    '''show main sequencer page'''
    if request.method == 'POST':
        form = ReferenceSelectForm(request.POST)
        if form.is_valid():
            reference_dna_model = form.cleaned_data['reference_dna']
            request.session['sequencer_reference'] = reference_dna_model.name
            return redirect('sequencer')
    else:
        form = ReferenceSelectForm()

    return render(request, 'dna/sequencer_reference_form.html', {'form': form})

def add_to_sequencer(request):
    '''add new data to sequencer'''
    # safety check first
    if not request.session.get('sequencer_reference', ''):
        return redirect('sequencer')

    if request.method == 'POST':
        form = PlainDNASampleForm(request.POST)
        if form.is_valid():
            dna_sample = form.cleaned_data['dna_sample']
            reference_model = get_object_or_404(ReferenceDNA,
                                                name=request.session.get('sequencer_reference'))
            sample = {'dna': dna_sample,
                      'offset': get_best_offset(reference_model.dna, dna_sample)}
            # appending directly to request.session['samples_data'] does not seem to work as expected
            try:
                tmp = request.session['samples_data']
            except KeyError:
                tmp = []
            tmp.append(sample)
            request.session['samples_data'] = tmp
            return redirect('sequencer')
    else:
        form = PlainDNASampleForm()

    return render(request, 'dna/sequencer_dna_sample_form.html', {'form': form})

def sequencer_result_for_print(request):
    '''show the sequencer result page'''
    if not (request.session.get('sequencer_reference', '')
            and request.session.get('samples_data', [])):
        return redirect('sequencer')

    reference_model = get_object_or_404(ReferenceDNA,
                                        name=request.session.get('sequencer_reference'))

    aligned_samples = align_samples(request.session['samples_data'])

    rows = get_output_rows(prepare_sequencer_data_for_display(reference_model.dna,
                                                              aligned_samples),
                           add_index_numbers=True,
                           separator_line=True)

#    return render(request, 'dna/sequencer_result.html')

    return render(request, 'dna/dna_matching_result_for_print.html',
                           {'reference_name': reference_model.name,
                            'rows': rows})

