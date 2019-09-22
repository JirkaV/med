from django import forms

class PrognozaForm(forms.Form):
    gly = forms.FloatField(label='Blood glucose level (mmol/l)', min_value=3.0, max_value=25.0)
    krea = forms.FloatField(label='Creatinine (μmol/l)', min_value=40.0, max_value=650.0)
    tc = forms.FloatField(label='Total cholesterol (mmol/l)', min_value=1.0, max_value=30.0)
    ldl = forms.FloatField(label='Low density cholesterol (mmol/l)', min_value=0.5, max_value=25.0)
    lp = forms.FloatField(label='Lipoprotein(a) (g/l)', min_value=0.05, max_value=150.0)
    viskpl = forms.FloatField(label='Plasma viscosity (mPa/s)', min_value=1.1, max_value=14.0)
    viskkr = forms.FloatField(label='Blood viscosity (mPa/s)', min_value=1.2, max_value=15.0)
