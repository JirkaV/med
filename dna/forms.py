from django import forms
from django.core.exceptions import ValidationError
from .models import ReferenceDNA
from .dna_values import DNA_ELEMENTS, VARIANTS

VALID = DNA_ELEMENTS + list(VARIANTS.keys())

class DNAField(forms.Field):
    '''custom class handling multiple IP addresses'''
    
    def validate(self, value):
        super(DNAField, self).validate(value)
        errors = []
        value = value.strip().upper()
        for element in value:
            if element not in VALID:
                errors.append('Invalid DNA - contains "%s"' % element)
                break
        if errors:
            raise ValidationError(errors)

class DNASampleForm(forms.Form):
    '''Form for DNA sample and reference DNA choice'''
    dna_sample = DNAField(label='',
                          widget=forms.widgets.Textarea(
                                           attrs={'class': 'input-xxlarge'}))
    reference_dna = forms.ModelChoiceField(label='Reference DNA',
                                           queryset=ReferenceDNA.objects.all(),
                                           empty_label=None)

class PlainDNASampleForm(forms.Form):
    '''Plain form displaying a single field for DNA sample'''
    dna_sample = DNAField(label='',
                          widget=forms.widgets.Textarea(
                                           attrs={'class': 'input-xxlarge'}))

class ReferenceSelectForm(forms.Form):
    '''Form for selecting reference DNA'''
    reference_dna = forms.ModelChoiceField(label='Reference DNA',
                                           queryset=ReferenceDNA.objects.all(),
                                           empty_label=None)
