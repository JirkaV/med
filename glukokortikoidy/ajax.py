from django.template.defaultfilters import floatformat
from dajaxice.core import dajaxice_functions
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from forms import GForm
from calculations import calculate_values

@dajaxice_register(method='POST')
def recalculate(request, field, value):
    '''recalculate form values'''
    dajax = Dajax()
    if not value:  # empty, avoid showing error message
        return dajax.json()  # empty

    # check that value is a float
    try:
        float(value)
    except ValueError:
        dajax.assign('#err_%s' % field, 'innerHTML', 'Not a number')
        dajax.add_css_class('#field_%s' % field, 'error')
        return dajax.json()

    new_values = calculate_values({field: value})
    fields = GForm().fields.keys()

    for f in fields:
        # clear errors
        dajax.remove_css_class('#field_%s' % f, 'error')
        dajax.assign('#err_%s' % f, 'innerHTML', '')
        if f == field:
            continue  # don't overwrite field the user is just editing 
        dajax.assign('#%s' % f, 'value', floatformat(new_values[f], arg=-2))

    return dajax.json()
