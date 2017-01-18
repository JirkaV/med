import pytest
from django.test import Client
from .utils import (get_best_offset as gbo,
                    get_triplets,
                    align_samples, get_output_rows,
                    get_differences_row as gdr,
                    convert_samples_to_row as cstr,
                    prepare_output_rows as por,
                    calculate_total_differences as ctd)
from .views import sequencer_delete_sample
from .forms import ReferenceInputForm, PlainDNASampleForm

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
    '''test the function for preparing output lines'''
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

def test_get_differences_row():
    '''test getting row outlining differences to reference'''
    assert gdr('', '') == ''
    assert gdr('A', ' ') == ' '
    assert gdr('A', 'A') == ' '
    assert gdr('A', 'T') == '*'
    assert gdr('A', 'B') == '*'  # "B" is not a variant for "A"
    assert gdr('A', 'X') == ':'  # X is any of AGCT
    assert gdr('AAA', ' A ') == '   '
    assert gdr('AAA', ' C ') == ' * '
    assert gdr('AAA', ' X ') == ' : '
    assert gdr('AAAAA', ' C X ') == ' * : '

def test_convert_samples_to_row():
    '''test that samples as dictionaries are correctly converted to strings'''
    assert cstr([], 0) == ''
    assert cstr([{'dna': 'A', 'offset': 0}], 1) == 'A'
    assert cstr([{'dna': 'A', 'offset': 0}], 2) == 'A '
    assert cstr([{'dna': 'A', 'offset': 1}], 2) == ' A'
    assert cstr([{'dna': 'C', 'offset': 2}], 5) == '  C  '
    assert cstr([{'dna': 'C', 'offset': 2},
                 {'dna': 'G', 'offset': 3}], 5) == '  CG '
    assert cstr([{'dna': 'CG', 'offset': 2},
                 {'dna': 'T', 'offset': 4}], 8) == '  CGT   '
    assert cstr([{'dna': 'CG', 'offset': 2},
                 {'dna': 'T', 'offset': 6}], 8) == '  CG  T '

@pytest.mark.django_db
def test_deleting_sample():
    '''test deleting sample from sequencer'''
    c = Client()
    # add some fake data to session
    samples_data = [{'dna': 'A', 'offset': 1},
                    {'dna': 'G', 'offset': 2},
                    {'dna': 'C', 'offset': 3},
                    {'dna': 'T', 'offset': 4}]
    sess = c.session  # can't assign directly to c.session, that does not work
    sess['sequencer_reference'] = ''
    sess['samples_data'] = samples_data
    sess.save()

    resp = c.get('/dna/sequencer/sample/delete/1/')
    assert c.session['samples_data'] == samples_data  # it was a GET request

    resp = c.post('/dna/sequencer/sample/delete/99/')
    assert c.session['samples_data'] == samples_data  # wrong index number

    resp = c.post('/dna/sequencer/sample/delete/1/')
    assert c.session['samples_data'] ==  [{'dna': 'G', 'offset': 2},
                                          {'dna': 'C', 'offset': 3},
                                          {'dna': 'T', 'offset': 4}]

    resp = c.post('/dna/sequencer/sample/delete/3/')
    assert c.session['samples_data'] ==  [{'dna': 'G', 'offset': 2},
                                          {'dna': 'C', 'offset': 3}]

def test_prepare_output_rows():
    '''test the prepare_output_rows utility function'''
    assert por('', []) == ['']
    assert por('', [{'dna': '', 'offset': 0}]) == ['', '', '']
    assert por('A', [{'dna': 'A', 'offset': 0}]) == ['A', 'A', ' ']
    assert por('AAA', [{'dna': 'A', 'offset': 0}]) == ['AAA', 'A  ', '   ']
    assert por('AAA', [{'dna': 'C', 'offset': 0}]) == ['AAA', 'C  ', '*  ']

    assert por('AAACCCAAA', [{'dna': 'CCC', 'offset': 3}]) == ['AAACCCAAA', '   CCC   ', '         ']
    assert por('AAACCCAAA', [{'dna': 'CAC', 'offset': 3}]) == ['AAACCCAAA', '   CAC   ', '    *    ']
    assert por('AAACCCAAA', [{'dna': 'CXC', 'offset': 3}]) == ['AAACCCAAA', '   CXC   ', '    :    ']
    assert por('AAACCCAAA', [{'dna': 'CXC', 'offset': 3},
                             {'dna': 'XCT', 'offset': 4} ]) == ['AAACCCAAA',
                                                                '   CXC   ',
                                                                '    :    ',
                                                                '    XCT  ',
                                                                '    : *  ']

def test_forms():
    '''test DNA input forms'''
    f = PlainDNASampleForm({'dna_sample': ''})
    assert not f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'A'})
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'AGCT'})
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'MRWSYKVHDBXN'})
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'E'})  # first letter that can't be in form
    assert not f.is_valid()
    f = PlainDNASampleForm({'dna_sample': '1'})
    assert not f.is_valid()
    f = PlainDNASampleForm({'dna_sample': '*'})
    assert not f.is_valid()

    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': ''})
    assert not f.is_valid()
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': 'A'})
    assert f.is_valid()
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': 'AGCT'})
    assert f.is_valid()
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': 'MRWSYKVHDBXN'})
    assert not f.is_valid()  # can't allow variants
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': 'E'})
    assert not f.is_valid()
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': '!'})
    assert not f.is_valid()
    f = ReferenceInputForm({'reference_dna_name': 'test',
                            'reference_dna_string': '*'})
    assert not f.is_valid()

def test_sample_longer_than_reference():
    '''test that forms won't allow sample longer then reference'''
    f = PlainDNASampleForm({'dna_sample': 'AAAA'})
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'AAAA'}, reference_length=999)
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'AAAA'}, reference_length=5)
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'AAAA'}, reference_length=4)
    assert f.is_valid()
    f = PlainDNASampleForm({'dna_sample': 'AAAA'}, reference_length=3)
    assert not f.is_valid()

def test_calculating_total_differences():
    '''test calculating number of differences'''
    assert ctd([]) == 0
    assert ctd(['']) == 0
    assert ctd(['', '']) == 0
    assert ctd(['*']) == 1
    assert ctd([':']) == 0  # variants are not differences
    assert ctd(['* ', ' *']) == 2  # one at beginning, one at end
    assert ctd(['* ', '* ']) == 1  # both differences are at the same offset
    assert ctd(['AAAAAAA',
                ' AGX AT',
                '  *:  *',
                '  XATGT',
                '  : ***']) == 4
