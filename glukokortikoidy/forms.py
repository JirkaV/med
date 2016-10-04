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

## all logic is not in JavaScript
#
#     def clean(self):
#         '''allow only one field'''
#         super(GForm, self).clean()
#         cnt = 0
#         for field_name in self.fields:
#             try:
#                 if self.data[field_name]:
#                     cnt += 1
#             except KeyError:
#                 pass
#         if cnt != 1:
#             raise ValidationError('Only and only one field must be entered!')
#         return self.cleaned_data
#
