from django.utils.timezone import now
from med.common.response import response
from forms import DNASampleForm
from utils import get_best_offset, get_diffs, get_triplets

def match_dna_sample(request):
    if request.method == 'POST':
        form = DNASampleForm(request.POST)
        if form.is_valid():
            dna_sample = form.cleaned_data['dna_sample']
            reference_dna = form.cleaned_data['reference_dna']
            ref_dna = reference_dna.dna
            ref_name = reference_dna.name 
            dna_sample = dna_sample.strip('\r\n').upper()
            best_offset = get_best_offset(ref_dna, dna_sample)
            changes = get_triplets(ref_dna, dna_sample, best_offset,
                                   different_only=True)

            # save data to session for print
            request.session['timestamp'] = now()
            request.session['best_offset'] = best_offset
            request.session['reference_dna'] = reference_dna
            request.session['changes'] = changes
            request.session['dna_sample'] = dna_sample

            return response(request, 'dna_matching_result.html',
                                      extra_context={'reference_name': ref_name,
                                                     'changes': changes})
    else:
        form = DNASampleForm()
    return response(request, 'dna_sample_form.html',
                              extra_context={'form': form})

def dna_comparison_for_print(request):
    try:
        # pick up data from session
        timestamp = request.session['timestamp']
        best_offset = request.session['best_offset']
        reference_dna = request.session['reference_dna']
        changes = request.session['changes']
        dna_sample = request.session['dna_sample']
    except KeyError:
        return response(request, 'dna_matching_result_for_print.html',
                              extra_context={'session_error': True})
    diffs = get_diffs(reference_dna.dna, dna_sample, best_offset,
                      show_index_numbers=True)
    return response(request, 'dna_matching_result_for_print.html',
                              extra_context={'reference': reference_dna,
                                             'changes': changes,
                                             'diffs': diffs,
                                             'timestamp': timestamp})
