from .utils import get_best_offset as gbo
from .utils import get_triplets
from .utils import align_samples, get_output_rows
from .utils import prepare_sample_for_display
from .utils import prepare_sequencer_data_for_display as psdd

TEST_DNA = 'AAAACCCCTTTTGGGG'
PRIMER1 = 'AACC'
PRIMER2 = 'TTGG'

def test_best_offset():
    '''test that best offset is located correctly'''
    REFERENCE = 'AAACCCCCCGGG'
    assert gbo(REFERENCE, 'T') == 0
    assert gbo(REFERENCE, 'A') == 0
    assert gbo(REFERENCE, 'CC') == 3
    assert gbo(REFERENCE, 'CG') == 8
    
def test_triplets():
    '''test that we get correct triplets'''
    assert get_triplets('AAA', 'GGG', 0) == [(True, 1, 'AAA', 'GGG')]
    assert get_triplets('ACGACTCGCGGG', 'ATTCGC', 3) == \
                                                 [(False, 1, 'ACG', '   '),
                                                  (True, 2, 'ACT', 'ATT'),
                                                  (False, 3, 'CGC', 'CGC'),
                                                  (False, 4, 'GGG', '   ')] 

    assert get_triplets('ACGACTCGC', 'ATT', 3, different_only=True) == \
                                                       [(True, 2, 'ACT', 'ATT')]

def test_offset_with_variants():
    '''test that best offset is located correctly'''
    REFERENCE = 'AAACCCCCCGGG'
    assert gbo(REFERENCE, 'Y') == 3  # Y -> C
    assert gbo(REFERENCE, 'K') == 9  # K -> G

# import time
# from .data import ABL_GEN_REFERENCE
# test_data = 'CAAGGTTTTCCTTCTCGCTGGACCCAGTGAAAATGACCCCAACCTTTTCGTTGCACTGTATGAAAAAGTGGCCAGTGGAGATAACACTCTAAGCATAACTAAAGGTGTTTTGCTCCGGGTCTTAGGCTATAATCACAATGGGGAATGGTGTGAAGCCCAAACCAAAAATGGCCAAGGCTCCCTCCCAAGCAACTACATCACGCCAGTCAACAGTCTGGAGAAACACTCCTGGTACCATGGGCCTGTGTCCCGCAATGCCGCTGAGTATCCGCTGAGCAGCAGGATCAATGGCAGCTTCTTGGTGCGTGAGAGTGAGAGCAGTCCTAGCCAGAGGTCCATCTCGCTGAGATACGAAGGGAGGGTGTACCATTACAGGATCCACACTGCTTCTGATGGCAAGCTCTACGTCTCCTCCGAGAGCCGCTTCAACACCCTGGCCGAGTTGGTTCATCATCATTCAACGGTGGCCGACGGGCTCATCACCACGCTCCAATATCCAGCCCCAAAGCGCAACAAGCCCACTGTCTATGGTGTGTCCCCCAACTACGACAAGTGGGAGATGGAACGCACGGACATCACCATGAAGCACAAGCTGGGCGGGGGCCAGTACGGGGAGGTGTACGAGGGCGTGTGGAAGAAATACAGCCTGACGGTGGCCGTGAAGACCTTGAAGGAGGACACCACGGAGGTGGAAGAGTTCTTGAAAGAAGCTGCAGTCATGAAAGAGATCAAACACCCTAACCTAGTGCAGCTCCTTGGGGTCTGCACCCGGGAGCCCCCGTTCTATATCATCACTGAGTTCCTGACCTACGGGAACCTCCTGGACTACCTGAGGGAGTGCAACCGGCAGGAGGTGAACGCCGTGGTGCTGCTGTACATGGCCACTCAGATCTCGTCAGCCATGGAGTACCTAGAGAAGAAAAACTTCATCCACAGAGATCTTGCTGCCCGAAACTGCCTGGTAGGGGAGAACCACTTGGTGAAGGTAGCTGATTTTGGCCTGAGCAGGTTGATGACAGGGGACACCTACACAGCCCATGCTGGAGCCAAGTTCCCCATCAAATGGACTGCACCCGAGAGCCTGGCCTACAACAAGTTCTCCATCAAGTCCGACGTCTGGGCATTTGGAGTATTGCTTTGGGAAATTGCTACCTATGGCATGTCCCCTTACCCGGGAATTGACCGTTCCCAGGTGTATGAGCTGCTAGAGAAGGACTACCGCATGAAGCGCCCAGAAGGCTGCCCAGAGAAGGTCTATGAACTCATGCGAGCATGTTGGCAGTGGAATCCCTCTGACCGGCCCTCCTTTGCTGAAATCCACCAAGCCTTTGAAACAATGTTCCAGGAATCCAGTATCTCAGACGAAGTGGAAAAGGAGCTGGGGAAACAAGGCGTCCGTGGGGCTGTGACTACCTTGCTGCAGGCCCCAGAGCTGCCCACCAAGACGAGGACCTCCAGGAGAGCTGCAGAGCACAGAGACACCACTGACGTGCCTGAGATGCCTCACTCCAAGGGCCAGGGAGAGAGCGATCCTCTGGACCATGAGCCTGCCGTGTCTCCATTGCTCCCTCGAAAAGAGCGAGGTCCCCCGGAGGGCGGCCTGAATGAAGATGAGCGCCTTCTCCCCAAAGACAAAAAGACCAACTTGTTCAGCGCCTTGATCAAGAAGAAGAAGAAGACAGCCCCAACCCCTCCCAAACGCAGCAGCTCCTTCCGGGAGATGGACGGCCAGCCGGAGCGCAGAGGGGCCGGCGAGGAAGAGGGCCGAGACATCAGCAACGGGGCACTGGCTTTCACCCCCTTGGACACAGCTGACCCAGCCAAGTCCCCAAAGCCCAGCAATGGGGCTGGGGTCCCCAATGGAGCCCTCCGGGAGTCCGGGGGCTCAGGCTTCCGGTCTCCCCACCTGTGGAAGAAGTCCAGCACGCTGACCAGCAGCCGCCTAGCCACCGGCGAGGAGGAGGGCGGTGGCAGCTCCAGCAAGCGCTTCCTGCGCTCTTGCTCCGTCTCCTGCGTTCCCCATGGGGCCAAGGACACGGAGTGGAGGTCAGTCACGCTGCCTCGGGACTTGCAGTCCACGGGAAGACAGTTTGACTCGTCCACATTTGGAGGGCACAAAAGTGAGAAGCCGGCTCTGCCTCGGAAGAGGGCAGGGGAGAACAGGTCTGACCAGGTGACCCGAGGCACAGTAACGCCTCCCCCCAGGCTGGTGAAAAAGAATGAGGAAGCTGCTGATGAGGTCTTCAAAGACATCATGGAGTCCAGCCCGGGCTCCAGCCCGCCCAACCTGACTCCAAAACCCCTCCGGCGGCAGGTCACCGTGGCCCCTGCCTCGGGCCTCCCCCACAAGGAAGAAGCCTGGAAAGGCAGTGCCTTAGGGACCCCTGCTGCAGCTGAGCCAGTGACCCCCACCAGCAAAGCAGGCTCAGGTGCACCAAGGGGCACCAGCAAGGGCCCCGCCGAGGAGTCCAGAGTGAGGAGGCACAAGCACTCCTCTGAGTCGCCAGGGAGGGACAAGGGGAAATTGTCCAAGCTCAAACCTGCCCCGCCGCCCCCACCAGCAGCCTCTGCAGGGAAGGCTGGAGGAAAGCCCTCGCAGAGGCCCGGCCAGGAGGCTGCCGGGGAGGCAGTCTTGGGCGCAAAGACAAAAGCCACGAGTCTGGTTGATGCTGTGAACAGTGACGCTGCCAAGCCCAGCCAGCCGGCAGAGGGCCTCAAAAAGCCCGTGCTCCCGGCCACTCCAAAGCCACACCCCGCCAAGCCGTCGGGGACCCCCATCAGCCCAGCCCCCGTTCCCCTTTCCACGTTGCCATCAGCATCCTCGGCCTTGGCAGGGGACCAGCCGTCTTCCACTGCCTTCATCCCTCTCATATCAACCCGAGTGTCTCTTCGGTTTTAAAGCCAGCCTCCAGAGCGGGCCAGCGGCGCCATCACCAAGGGCGT'
# def test_speed():
#     start_time = time.time()
#     print(gbo(ABL_GEN_REFERENCE, test_data))
#     print('{:.3f}'.format(time.time() - start_time))
#     assert False
#

def test_samples_aligning():
    '''test aligning samples to least number of lines'''
    data = [{'dna': 'A', 'offset': 0}]
    assert align_samples(data) == [data]

    data = [{'dna': 'A', 'offset': 1}]
    assert align_samples(data) == [data]

    data = [{'dna': 'A', 'offset': 1},
            {'dna': 'C', 'offset': 2}]
    assert align_samples(data) == [data]  # we rely on the "correct" dictionary comparison here

    # reversed
    data = [{'dna': 'C', 'offset': 2},
            {'dna': 'A', 'offset': 1}]
    assert align_samples(data) == [[{'dna': 'A', 'offset': 1},
                                    {'dna': 'C', 'offset': 2}]]

    data = [{'dna': 'A', 'offset': 1},
            {'dna': 'C', 'offset': 1}]
    assert align_samples(data) == [[{'dna': 'A', 'offset': 1}],
                                   [{'dna': 'C', 'offset': 1}]]

    data = [{'dna': 'AAAA', 'offset': 1},
            {'dna': 'CCCC', 'offset': 5}]
    assert align_samples(data) == [data]  # we rely on the "correct" dictionary comparison here

    data = [{'dna': 'AAAA', 'offset': 1},
            {'dna': 'CCCC', 'offset': 4}]
    assert align_samples(data) == [[{'dna': 'AAAA', 'offset': 1}],
                                   [{'dna': 'CCCC', 'offset': 4}]]

    data = [{'dna': 'AAAGGG', 'offset': 1},
            {'dna': 'GGGCCC', 'offset': 4},
            {'dna': 'CCCTTT', 'offset': 7},
            {'dna': 'TTT',    'offset': 10}]
    assert align_samples(data) == [[{'dna': 'AAAGGG', 'offset': 1}, {'dna': 'CCCTTT', 'offset': 7}],
                                   [{'dna': 'GGGCCC', 'offset': 4}, {'dna': 'TTT',    'offset': 10}]]

    data = [{'dna': 'AAAGGGCCC', 'offset': 1},
            {'dna': 'GGGCCC',    'offset': 4},
            {'dna': 'GC',        'offset': 6},
            {'dna': 'C',         'offset': 7}]
    assert align_samples(data) == [[{'dna': 'AAAGGGCCC', 'offset': 1}],
                                   [{'dna': 'GGGCCC',    'offset': 4}],
                                   [{'dna': 'GC',        'offset': 6}],
                                   [{'dna': 'C',         'offset': 7}]]

def test_get_rows():
    '''test the get_rows() function for preparing output lines'''
    assert get_output_rows(['']) == []
    assert get_output_rows(['A']) == ['A']
    assert get_output_rows(['A'*160]) == ['A'*80, 'A'*80]
    assert get_output_rows(['A'*10], width=5) == ['A'*5, 'A'*5]
    assert get_output_rows(['A'*10], width=5, separator_line=True) == ['A'*5, ' '*5, 'A'*5]
    assert get_output_rows(['A'*10, 'T'*10], width=5) == ['A'*5, 'T'*5, 'A'*5, 'T'*5]
    assert get_output_rows(['A'*10, ' '*10], width=5) == ['A'*5, ' '*5, 'A'*5, ' '*5]
    assert (get_output_rows(['A'* 10, ' '*10], width=5, collapse_empty_lines=True) ==
            ['AAAAA', ' ', 'AAAAA', ' '])
    assert (get_output_rows(['A'*10, 'T'*10], width=5, add_index_numbers=True) ==
            ['     1 AAAAA      5',
             '       TTTTT       ',
             '     6 AAAAA     10',
             '       TTTTT       '])
    assert (get_output_rows(['A'*10, 'T'*10], width=5,
                            add_index_numbers=True, separator_line=True) ==
            ['     1 AAAAA      5',
             '       TTTTT       ',
             '                   ',
             '     6 AAAAA     10',
             '       TTTTT       '])

    assert (get_output_rows(['A'*10, ' '*10], width=5,
                            collapse_empty_lines=True,
                            add_index_numbers=True) ==
            ['     1 AAAAA      5',
             ' ',
             '     6 AAAAA     10',
             ' '])
    assert (get_output_rows(['A'*10, ' '*10], width=5,
                             collapse_empty_lines=True,
                             add_index_numbers=True,
                             separator_line=True) ==
            ['     1 AAAAA      5',
             ' ',
             ' ',
             '     6 AAAAA     10',
             ' '])

    assert (get_output_rows(['A'*3, 'C'*3, 'G'*3, 'T'*3], width=1) ==
            ['A', 'C', 'G', 'T', 'A', 'C', 'G', 'T', 'A', 'C', 'G', 'T'])

def test_prepare_sample_for_display():
    '''test that the prepare_sample_for_display() works as expected'''
    assert prepare_sample_for_display('', '', 0) == ['', '', '']
    assert (prepare_sample_for_display('A', 'A', 0) ==
            ['A', 'A', ' '])
    assert (prepare_sample_for_display('AAA', 'A', 0) ==
            ['AAA', 'A  ', '   '])
    assert (prepare_sample_for_display('AAA', 'C', 0) ==
            ['AAA', 'C  ', '*  '])
    reference = 'AAACCCAAA'
    assert (prepare_sample_for_display(reference, 'CCC', 3) ==
            ['AAACCCAAA', '   CCC   ', '         '])
    assert (prepare_sample_for_display(reference, 'CAC', 3) ==
            ['AAACCCAAA', '   CAC   ', '    *    '])
    assert (prepare_sample_for_display(reference, 'CXC', 3) ==
            ['AAACCCAAA', '   CXC   ', '    :    '])

def test_prepare_sequencer_data_for_display():
    '''test that sequencer data can be preprocessed for final display'''
    assert psdd('', [[]]) == ['', '']
    assert psdd('A', [[{'dna': 'A', 'offset': 0}]]) == ['A', 'A']
    assert psdd('AACGT', [[{'dna': 'C', 'offset': 2}]]) == ['AACGT', '  C  ']
    assert psdd('AACGT', [[{'dna': 'C', 'offset': 2},
                           {'dna': 'G', 'offset': 3}]]) == ['AACGT', '  CG ']
    assert psdd('AACGT', [[{'dna': 'CG', 'offset': 2},
                           {'dna': 'T', 'offset': 4}],
                           [{'dna': 'GT', 'offset': 3}]]) == ['AACGT', '  CGT', '   GT']
