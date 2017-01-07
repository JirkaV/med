from difflib import SequenceMatcher
from .dna_values import VARIANTS
from .data import *

FILL_CHAR = ' '  # added to sample on left and right to match reference length
DIFF_CHAR = '*'  # display where sample is different from reference
SAME_CHAR = ' '  # display where sample matches reference
VARIANT_CHAR = ':'  # display where sample matches reference, but was a variant match

def _count_failures(r, s, min_previous_failures):
    '''returns number failures (mismatches) between reference cut and sample.
    May return falsely big number to indicate early bailout if current result
    is already worse then best known previous result'''
    # this code is heavily optimized for speed, do not change without
    # speed testing  (tested on CPython 3.5)
    len_s = len(s)
    failures = 0
    for x in range(len_s):
        r_x = r[x]  # reduce array lookups below
        s_x = s[x]
        if r_x != s_x:
            if not (s_x in VARIANTS and r_x in VARIANTS[s_x]):
                failures += 1
                if failures >= min_previous_failures:
                    return len_s  # no point in returning the actual number
    return failures

def get_best_offset(reference, sample):
    '''returns best offset so it best matches reference
    (has least number of differences.
    '''
    offset, best_offset, least_failures = 0, 0, len(sample)
    len_diff = len(reference) - len(sample)
    assert len_diff >= 0, '[!] Sample is longer than reference!'

    # note - passing reference[offset:] to _count_failures is quicker than
    # passing the original reference + offset number
    # and using "r_x = r[offset+x]" in _count_failures

    while offset < len_diff:
        failures = _count_failures(reference[offset:], sample, least_failures)
        if failures < least_failures:
            best_offset = offset
            least_failures = failures
        offset += 1
    return best_offset

def _fill_to_len(reference_, sample_, sample_offset_):
    '''left- and right-fills sample with spaces so len(sample) == len(reference)
    as it makes other functions much more simple
    '''
    assert len(reference_) >= len(sample_) + sample_offset_
    return '%s%s%s' % (FILL_CHAR * sample_offset_, 
                    sample_, 
               FILL_CHAR * (len(reference_) - (len(sample_) + sample_offset_)))
    
def _get_diffs(a, b):
    '''returns a string constructed using DIFF_CHAR and SAME_CHAR'''
    len_a = len(a)
    assert len_a == len(b)
    res = []
    i = 0
    while i < len_a:
        if a[i] == FILL_CHAR:
            tmp = SAME_CHAR
        elif a[i] == b[i]:
            tmp = SAME_CHAR
        elif a[i] in VARIANTS.keys() and b[i] in VARIANTS[a[i]]:
            tmp = VARIANT_CHAR
        else:
            tmp = DIFF_CHAR
        res.append(tmp)
        i += 1
    return ''.join(res)

def get_diffs(reference, sample, sample_offset, width=80,
              insert_blank_lines=True,
              show_index_numbers=True):
    '''prepares visual representation of DNA differences'''
    r = reference
    s = _fill_to_len(reference, sample, sample_offset)
    res = []
    curr_index = 0
    while r:
        rcut, r = r[:width], r[width:]
        scut, s = s[:width], s[width:]
        diffs = _get_diffs(scut, rcut)
        if show_index_numbers:
            rcut = '%s %s %s' % ('%6i' % (curr_index + 1),
                                 rcut,
                                 '%6i' % (curr_index + width))
            scut = '%s %s %s' % (' '*6,
                                 scut,
                                 ' '*6)
            diffs = '%s %s %s' % (' '*6,
                                  diffs,
                                  ' '*6)
        res.extend([rcut, scut, diffs])
        if not show_index_numbers and insert_blank_lines:
            res.append(' ')  # one space to keep <pre> in HTML happy. We only
                             # need to do this is show_index_numbers is False
                             # as it inserts blanks anyway
        curr_index += width
    return res

def display_diffs(*args, **kwargs):
    '''provides visual representation of DNA differences'''
    diffs = get_diffs(*args, **kwargs)
    for diff in diffs:
        print(diff)

def get_triplets(reference, sample, sample_offset, different_only=False):
    '''cuts reference and sample to sections of three (slicing done
    on reference) and returns list of tuples 
    (changed, index, ref_slice, sample_slice).
    
    Index is positional number of the triplet in the reference, starting from 1.
    
    Sample slice may will contain spaces where there is no sample data for 
    that section of reference. Changed is False in this case.
    
    This is useful for figuring out which sections are different to find
    mutations in DNA.
    
    Example:
        get_triplets('ACGACTCGC', 'ATT', 3) = [(False, 0, 'ACG', '   '),
                                               (True, 3, 'ACT', 'ATT'),
                                               (False, 6, 'CGC', '   ')]
    '''
    r = reference
    s = _fill_to_len(r, sample, sample_offset)
    idx = 1  # index from 1 as it's for humans
    res = []
    while r:
        r_slice, r = r[:3], r[3:]
        s_slice, s = s[:3], s[3:]
        # we only say r_slice and s_slice are different if s_slice
        # contains no spaces and really is different from r_slice
        # variants in sample are ignored (shown as a difference)
        #
        # it is OK to *not* display changes in the first or last kodon (triplet)
        # if they are incomplete, so ignoring anything with len < 3 is fine
        # (verified with the customer)
        if len(s_slice.strip()) == 3 and s_slice != r_slice:
            different = True
        else:
            different = False
        if different or not different_only:
            res.append((different, idx, r_slice, s_slice)) # (( )) - add tuple
        idx += 1
    return res

def fill_database():
    from .models import ReferenceDNA
    for name, reference_dna in REFERENCE_DATA:
         _, created = ReferenceDNA.objects.get_or_create(name=name, dna=reference_dna)
         if created:
            print('created {}'.format(name))
