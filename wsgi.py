import sys
import os
import site

# workaround for various print messages stopping the app under mod_wsgi (namely South)
sys.stdout = sys.stderr

site.addsitedir('/data/webapps/virt_med/lib/python2.6/site-packages')
sys.path.append('/data/webapps')
sys.path.append('/data/webapps/med')

os.environ['DJANGO_SETTINGS_MODULE'] = 'med.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
