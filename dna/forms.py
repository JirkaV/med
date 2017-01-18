from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .models import ReferenceDNA
from .dna_values import DNA_ELEMENTS, VARIANTS

VALID_WITH_VARIANTS = DNA_ELEMENTS + list(VARIANTS.keys())

class DNAWithVariantsField(forms.Field):
    '''form field for DNA input with possible variants characters'''
    
    def validate(self, value):
        super().validate(value)
        errors = []
        value = value.strip().upper()
        for element in value:
            if element not in VALID_WITH_VARIANTS:
                errors.append('Invalid DNA - contains "%s"' % element)
                break
        if errors:
            raise ValidationError(errors)

class StrictDNAField(forms.Field):
    '''form field for strict DNA input, only allowing the classic "AGCT" chars'''

    def validate(self, value):
        super().validate(value)
        errors = []
        value = value.strip().upper()
        for element in value:
            if element not in DNA_ELEMENTS:
                errors.append('Invalid DNA - contains "%s"' % element)
                break
        if errors:
            raise ValidationError(errors)

class DNASampleBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        reference_length = kwargs.pop('reference_length', None)
        super().__init__(*args, **kwargs)
        if reference_length is not None:
            self.fields['dna_sample'].validators.append(validators.MaxLengthValidator(reference_length))
            self.fields['dna_sample'].help_text='Please enter up to {} nucleotides (reference length)'.format(reference_length)

    dna_sample = DNAWithVariantsField(label='',
                                      widget=forms.widgets.Textarea(
                                            attrs={'class': 'input-xxlarge'}))

class DNASampleForm(DNASampleBaseForm):
    '''Form for DNA sample and reference DNA choice'''
    reference_dna = forms.ModelChoiceField(label='Reference DNA',
                                           queryset=ReferenceDNA.objects.all(),
                                           empty_label=None)

class PlainDNASampleForm(DNASampleBaseForm):
    '''Plain form displaying a single field for DNA sample'''

class ReferenceSelectForm(forms.Form):
    '''Form for selecting reference DNA'''
    reference_dna = forms.ModelChoiceField(label='Reference DNA',
                                           queryset=ReferenceDNA.objects.all(),
                                           empty_label=None)

class ReferenceInputForm(forms.Form):
    '''Form for selecting reference DNA'''
    reference_dna_name = forms.CharField(label='Reference name',
                                         min_length=2,
                                         max_length=40)
    reference_dna_string = StrictDNAField(label='',
                                          widget=forms.widgets.Textarea(
                                                   attrs={'class': 'input-xxlarge'}))
