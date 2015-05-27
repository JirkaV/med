# -*- coding: utf-8 -*-
import sys
import django
from pgs.bal.models import *

django.setup()

if __name__ == '__main__':
    p = Pacient.objects.get(rc=sys.argv[1])
    dg, _ = Diagnoza.objects.get_or_create(kod=sys.argv[2])
    p.dg = dg
    p.save()
    print p.rc, p.dg
