from calculations import calculate_values as _c
from forms import GForm

def test_base_values():
    '''test base values'''
    assert _c({}) == {
        'betamethason': 0.75,
        'cortison': 25.0,
        'dexamethason': 0.75,
        'hydrocortison': 20.0,
        'metylprednisolon': 4.0,
        'prednisolon': 5.0,
        'prednison': 5.0,
        'triamcinolon': 4.0,
    }

def test_multiple_entries():
    '''test that we don't accept multiple entries'''
    try:
        assert _c({'cortison': 50.0, 'prednison': 10.0})
        assert False
    except ValueError:
        pass

def test_calculated_values():
    '''test base values'''
    assert _c({'cortison': 50.0}) == {
        'betamethason': 1.5,
        'cortison': 50.0,
        'dexamethason': 1.5,
        'hydrocortison': 40.0,
        'metylprednisolon': 8.0,
        'prednisolon': 10.0,
        'prednison': 10.0,
        'triamcinolon': 8.0,
    }

    assert _c({'prednison': 100}) == {
        'betamethason': 15.0,
        'cortison': 500.0,
        'dexamethason': 15.0,
        'hydrocortison': 400.0,
        'metylprednisolon': 80.0,
        'prednisolon': 100.0,
        'prednison': 100.0,
        'triamcinolon': 80.0,
    }

def test_multiple_field_entry():
    '''test that only one field can be entered'''
    f = GForm({'cortison': 50.0})
    assert f.is_valid()
    f = GForm({'cortison': 50.0, 'prednison': 10.0})
    assert not f.is_valid()
