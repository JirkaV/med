from django.shortcuts import render
from django.template.defaultfilters import date as template_date
from django.utils.timezone import now
from .forms import DNASampleForm
from .utils import get_best_offset, get_diffs, get_triplets

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
        changes = request.session['changes']
        dna_sample = request.session['dna_sample']
    except KeyError:
        return render(request, 'dna/dna_matching_result_for_print.html',
                              {'session_error': True})
    diffs = get_diffs(reference_dna, dna_sample, best_offset,
                      show_index_numbers=True)
    return render(request, 'dna/dna_matching_result_for_print.html',
                           {'reference': reference_dna,
                            'changes': changes,
                            'diffs': diffs,
                            'timestamp_string': timestamp})
