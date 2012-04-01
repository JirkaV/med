from django.views.generic.simple import direct_to_template
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
            diffs = get_diffs(ref_dna, dna_sample, best_offset,
                              show_index_numbers=True)
            changes = get_triplets(ref_dna, dna_sample, best_offset,
                                   different_only=True)
            return direct_to_template(request, 'dna_matching_result.html', 
                                      extra_context={'reference': ref_name,
                                                     'diffs': diffs,
                                                     'changes': changes})
    else:
        form = DNASampleForm()
    return direct_to_template(request, 'dna_sample_form.html', 
                              extra_context={'form': form})
