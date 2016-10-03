#  from .utils import get_sequence_between_primers as gsbp  - not really needed for production
from .utils import get_best_offset as gbo
from .utils import get_triplets

TEST_DNA = 'AAAACCCCTTTTGGGG'
PRIMER1 = 'AACC'
PRIMER2 = 'TTGG'

# def test_sequence_between_primers():
#     '''test that searching primers in reference works'''
#     assert gsbp(TEST_DNA, 'AGC', 'CGA') == None
#     assert gsbp(TEST_DNA, PRIMER1, PRIMER2) == 'AACCCCTTTTGG'

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
