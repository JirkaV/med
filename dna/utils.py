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

def get_output_rows(list_of_strings,
                    width=80,
                    add_index_numbers=False,
                    collapse_empty_lines=False):
    '''given list of strings (all expected to be of same length, returns
    list of rows of desired width, optionally including index number
    for better orientation where the original strings alternate in rows
    '''
    res = []
    length = len(list_of_strings[0])  # all expected to be of same length
    curr = 0
    while curr < length:
        for i, curr_string in enumerate(list_of_strings):
            line = curr_string[curr:curr+width]
            if add_index_numbers:
                if i == 0:  # line that needs index numbers
                    line = '{:>6} {} {:>6}'.format(curr+1, line, curr+width)
                else:
                    line = '{} {} {}'.format(' '*6, line, ' '*6)
            if collapse_empty_lines and not line.strip():
                line = ' '  # we need to keep at least one space for <pre> to work
            res.append(line)
        curr += width
    return res

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
    s = '{}{}{}'.format(FILL_CHAR*sample_offset,
                        sample,
                        FILL_CHAR*(len(r)-(len(sample)+sample_offset)))

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

def align_samples(samples):
    '''tries to align existing samples to least possible number of lines
    for later display (so they don't overlap), e.g.

    AAGGGATCGGATCGA        CGATCGATCTCGGATCG   CCGATCGGCTAGCTTGCG
              ATCGACTTAGGCTCGAT           CGACGCCGATC
    returns list (one per line) of lists (containings samples on the line)
    '''
    res = []
    todo = samples[:]
    todo.sort(key=lambda x: x['offset'])  # sort by offset
    while todo:
        last_offset = 0
        todo_copy = todo[:]
        todo = []
        thisline = []
        for sample in todo_copy:
            if sample['offset'] >= last_offset:
                thisline.append(sample)
                last_offset = sample['offset'] + len(sample['dna'])
            else:
                todo.append(sample)
        res.append(thisline)
    return res

def prepare_sample_for_display(reference, sample, sample_offset):
    '''given reference, sample and offset returns list of 3 strings suitable
    for get_output_rows() where:
        * first row is reference unchanged
        * second row is sample at proper offset extended to proper length
          using FILL_CHAR
        * third row is appropriately composed of SAME_CHAR, DIFF_CHAR
          and VARIANT_CHAR at proper places
    '''
    lfill = FILL_CHAR*sample_offset
    rfill = FILL_CHAR*(len(reference)-(sample_offset+len(sample)))
    thirdrow_chars = []
    for i, char in enumerate(sample):
        if char == reference[sample_offset+i]:
            thirdrow_chars.append(SAME_CHAR)
        else:
            if char in VARIANTS:
                thirdrow_chars.append(VARIANT_CHAR)
            else:
                thirdrow_chars.append(DIFF_CHAR)
    return [reference,
            '{}{}{}'.format(lfill, sample, rfill),
            '{}{}{}'.format(lfill, ''.join(thirdrow_chars), rfill)]

def prepare_sequencer_data_for_display(reference, aligned_samples):
    '''takes reference and samples aligned using align_samples()
    and prepares data for get_output_rows()
    '''
    res = [reference]
    for samples_line in aligned_samples:
        tmp = []
        last_offset = 0
        for elem in samples_line:
            wanted = elem['offset']
            tmp.append(FILL_CHAR*(wanted-last_offset))
            tmp.append(elem['dna'])
            last_offset = elem['offset'] + len(elem['dna'])
        tmp = ''.join(tmp)
        tmp += FILL_CHAR*(len(reference)-len(tmp))
        res.append(tmp)
    return res
