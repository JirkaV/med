from django import forms

class PrognozaForm(forms.Form):
    gly = forms.FloatField(label='Blood glucose level (mmol/l)', min_value=3.7, max_value=10.6)
    krea = forms.FloatField(label='Creatinine (μmol/l)', min_value=55.0, max_value=126.0)
    tc = forms.FloatField(label='Total cholesterol (mmol/l)', min_value=2.5, max_value=6.9)
    ldl = forms.FloatField(label='Low density cholesterol (mmol/l)', min_value=1.02, max_value=4.7)
    lp = forms.FloatField(label='Lipoprotein(a) (g/l)', min_value=0.01, max_value=3.0)
    viskpl = forms.FloatField(label='Plasma viscosity (mPa/s)', min_value=1.62, max_value=3.72)
    viskkr = forms.FloatField(label='Blood viscosity (mPa/s)', min_value=4.14, max_value=10.19)
