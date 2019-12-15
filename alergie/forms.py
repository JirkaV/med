from django import forms

class CheckForm(forms.Form):
    text = forms.CharField(min_length=5, max_length=8192,
                           label='',
                           widget=forms.widgets.Textarea(
                                  attrs={'class': 'input-xxlarge'}))
