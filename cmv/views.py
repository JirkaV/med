from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib import messages
from forms import UploadForm
from imports import process_xlsx
from models import Pacient

def prehled(request):
    return direct_to_template(request,
                              'prehled.html',
                              extra_context={'pacienti': Pacient.objects.all()})

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            xls_data = process_xlsx(request.FILES['file'])
            p, created = Pacient.objects.get_or_create(rc=xls_data['rc'])
            p.jmeno = xls_data['jmeno']
            p.prijmeni = xls_data['prijmeni']
            p.json_data = simplejson.dumps(xls_data['data'])
            p.save()

            if created:
                messages.success(request, 'Pacient %s pridan' % p)
            else:
                messages.success(request, 'Pacient %s upraven' % p)

            return HttpResponseRedirect(reverse('cmv_prehled'))
    form = UploadForm()
    return direct_to_template(request,
                              'xlsx_upload.html',
                              extra_context={'form': form})
