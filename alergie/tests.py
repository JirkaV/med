from matcher import find_matches

def test_matcher():
    assert find_matches('') == []
    assert find_matches('Bronopol') == ['Bronopol']
    assert find_matches('bronopol') == ['bronopol']
    assert find_matches(' bronopol ') == ['bronopol']

    assert find_matches('some bronopol recipe') == ['bronopol']

