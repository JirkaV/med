from django.shortcuts import render
from .forms import CheckForm
from .matcher import find_matches

def check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            matches = find_matches(form.cleaned_data['text'])
            return render(request,
                          'alergie/result.html',
                          {'matches': matches})
    else:
        form = CheckForm()
    return render(request, 'alergie/index.html', {'form': form})
