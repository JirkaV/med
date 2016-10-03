# -*- coding: UTF-8 -*-

from django.shortcuts import render
from .forms import GForm
from .calculations import calculate_values

def calculator(request):
    if request.method == 'POST':
        form = GForm(request.POST)
        if form.is_valid():
            recalculated_data = calculate_values(form.cleaned_data)
            return render(request, 'glukokortikoidy.html',
                                   {'data': recalculated_data})
    else:
        form = GForm()
    return render(request, 'glukokortikoidy/form.html',
                              {'form': form})
