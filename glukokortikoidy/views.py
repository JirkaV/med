# -*- coding: UTF-8 -*-

from django.views.generic.simple import direct_to_template
from forms import GForm
from calculations import calculate_values

def calculator(request):
    if request.method == 'POST':
        form = GForm(request.POST)
        if form.is_valid():
            recalculated_data = calculate_values(form.cleaned_data)
            return direct_to_template(request, 'glukokortikoidy.html',
                                      extra_context={'data': recalculated_data})
    else:
        form = GForm()
    return direct_to_template(request, 'glukokortikoidy_form.html', 
                              extra_context={'form': form})
                                                                                        
