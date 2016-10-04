# -*- coding: UTF-8 -*-

from django.shortcuts import render
from .forms import GForm

def calculator(request):
    form = GForm()
    return render(request, 'glukokortikoidy/form.html',
                              {'form': form})
