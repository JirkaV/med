from django import forms
from django.core.exceptions import ValidationError
from models import ReferenceDNA

DNA_ELEMENTS = ('A', 'C', 'G', 'T')

class DNAField(forms.Field):
    '''custom class handling multiple IP addresses'''
    
    def validate(self, value):
        super(DNAField, self).validate(value)
        errors = []
        value = value.strip().upper()
        for element in value:
            if element not in DNA_ELEMENTS:
                errors.append('Invalid DNA - contains "%s"' % element)
                break
        if errors:
            raise ValidationError(errors)

class DNASampleForm(forms.Form):
    '''Simple form displaying a single text field'''
    dna_sample = DNAField(label='',
                          widget=forms.widgets.Textarea(
                                                 attrs={'cols':40, 'rows':20}))

#     reference = forms.ChoiceField(choices=(('54', 'UL54'),
#                                            ('97', 'UL97')))
    reference_dna = forms.ModelChoiceField(label='Reference DNA',
                                           queryset=ReferenceDNA.objects.all(),
                                           empty_label=None)
