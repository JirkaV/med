from django import forms
from django.core.exceptions import ValidationError

class GForm(forms.Form):
    '''form for data entry'''
    metylprednisolon = forms.FloatField(min_value=0.0, required=False)
    hydrocortison = forms.FloatField(min_value=0.0, required=False)
    dexamethason = forms.FloatField(min_value=0.0, required=False)
    prednison = forms.FloatField(min_value=0.0, required=False)
    prednisolon = forms.FloatField(min_value=0.0, required=False)
    cortison = forms.FloatField(min_value=0.0, required=False)
    betamethason = forms.FloatField(min_value=0.0, required=False)
    triamcinolon = forms.FloatField(min_value=0.0, required=False)
