# -*- coding: UTF-8 -*-

from django.shortcuts import render
from .forms import PrognozaForm
from .stats import calculate_linear, calculate_quadratic

def index(request):
    form = PrognozaForm(request.GET or None)
    if form.is_valid():
        return render(request, 'prognoza/result.html',
                              {'data': form.cleaned_data,
                               'result_linear': calculate_linear(form.cleaned_data),
                               'result_quadratic': calculate_quadratic(form.cleaned_data)})
    return render(request, 'prognoza/form.html',
                              {'form': form})
