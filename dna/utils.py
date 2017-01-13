from .dna_values import VARIANTS

FILL_CHAR = ' '  # added to sample on left and right to match reference length
DIFF_CHAR = '*'  # display where sample is different from reference
SAME_CHAR = ' '  # display where sample matches reference
VARIANT_CHAR = ':'  # display where sample matches reference, but was a variant match

def fill_database():
    from .models import ReferenceDNA
    from .data import REFERENCE_DATA
    for name, reference_dna in REFERENCE_DATA:
        _, created = ReferenceDNA.objects.get_or_create(name=name, dna=reference_dna)
        if created:
            print('created {}'.format(name))

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
        different = bool(len(s_slice.strip()) == 3 and s_slice != r_slice)
        if different or not different_only:
            res.append((different, idx, r_slice, s_slice)) # (( )) - add tuple
        idx += 1
    return res

def get_differences_row(reference, samples_row):
    '''takes row (which is expected to be of the same length as reference)
    and probably sample or multiple samples wrapped in spaces
    and returns row of the same length having SAME_CHAR, DIFF_CHAR or
    VARIANT_CHAR at correct places
    '''
    res = []
    for r, s in zip(reference, samples_row):
        if r == s or s == FILL_CHAR:
            res.append(SAME_CHAR)
        else:
            if s in VARIANTS:
                res.append(VARIANT_CHAR)
            else:
                res.append(DIFF_CHAR)
    return ''.join(res)

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

def convert_samples_to_row(samples, expected_length):
    '''takes samples in {'dna': 'X', 'offset': Y} format and returns
    a string that is a basis for future output.

    Samples are expected to be sorted smallest to highest offset and
    non-overlapping (see align_samples())

    The resulting string is then lenghtened as needed to have expected_length
    (usually the reference DNA length)
    '''
    res = []
    last_offset = 0
    for sample in samples:
        res.append(FILL_CHAR*(sample['offset']-last_offset))
        res.append(sample['dna'])
        last_offset = sample['offset'] + len(sample['dna'])
    res.append(FILL_CHAR*(expected_length-last_offset))
    return ''.join(res)

def prepare_output_rows(reference, samples):
    '''given reference as string and samples as list of dictionaries returns
    minimum number of rows suitable for output (get_output_rows())
    '''
    res = [reference]
    ref_len = len(reference)
    aligned_samples = align_samples(samples)
    for aligned_samples_row in aligned_samples:
        samples_row_string = convert_samples_to_row(aligned_samples_row, ref_len)
        res.extend([samples_row_string,
                    get_differences_row(reference, samples_row_string)])
    return res

def get_output_rows(list_of_strings,
                    width=80,
                    add_index_numbers=False,
                    collapse_empty_lines=False,
                    separator_line=False):
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
                line = FILL_CHAR  # we need to keep at least one space for <pre> to work
            res.append(line)
        curr += width
        if separator_line and curr < length:  # don't add separator as last line
            # width+14 is for line + 6-chars aligned index on each side separated by a space
            res.append(FILL_CHAR*(1 if collapse_empty_lines else width+14 if add_index_numbers else width))
    return res
