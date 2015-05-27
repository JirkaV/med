# -*- coding: cp1250 -*-

# import datetime
#
# def rc2datum(rc_):
#     d = rc_[:6]
#     if d[2] == '5':
#         d = d[:2] + '0' + d[3:]
#     if d[2] == '6':
#         d = d[:2] + '1' + d[3:]
#     datum = datetime.datetime.strptime(d, '%y%m%d').date()
#     print datum
#
# print rc2datum('760208/2411')
# print rc2datum('835120/1234')

from django.db.models import Count, F, Q
from pgs.bal.models import *

# m, z = 0, 0
# odbery = 0
# pacienti = 0
# for p in Pacient.objects.filter(datum_transplantace__isnull=False):
#     use = False
#     for o in p.odber_set.all():
#         if o.datum > p.datum_transplantace:
#             use = True
#             odbery += 1
#     if not use:
#         print 'skipping', p
#         continue
#     pacienti += 1
#     if p.rc[2] in ['0', '1']:
#         m += 1
#     elif p.rc[2] in ['5', '6']:
#         z += 1
#     else:
#         print 'Huh?', p.rc
# print odbery
# print pacienti
# print m, z

## nejmladsi v dobe odberu
# nejmladsi = None
# for o in Odber.objects.all():
#     if not o.pacient.datum_transplantace or o.pacient.datum_transplantace > o.datum:
#         continue
#     vek = o.datum - o.pacient.datum_narozeni
#     if nejmladsi is None or vek < nejmladsi:
#         nejmladsi = vek
#         nejmladsi_pacient = o.pacient
# print 'Nejmladsi pacient v den odberu:', nejmladsi_pacient
# print 'Vek v den odberu:', nejmladsi.days // 365


## nejstarsi v dobe odberu
# nejstarsi = None
# for o in Odber.objects.all():
#     if not o.pacient.datum_transplantace or o.pacient.datum_transplantace > o.datum:
#         continue
#     vek = o.datum - o.pacient.datum_narozeni
#     if nejstarsi is None or vek > nejstarsi:
#         nejstarsi = vek
#         nejstarsi_pacient = o.pacient
# print 'nejstarsi pacient v den odberu:', nejstarsi_pacient
# print 'Vek v den odberu:', nejstarsi.days // 365

#  # kategorie veku
# res = [0 for x in range(10)]
# print res
# hotovi = set()
# for o in Odber.objects.all().order_by('datum'):
#     if not o.pacient.datum_transplantace or o.pacient.datum_transplantace > o.datum:
#         continue
#     if o.pacient in hotovi:
#         continue
#     hotovi.add(o.pacient)
#     vek = (o.datum - o.pacient.datum_narozeni).days // 365
#     kategorie = vek / 10
#     res[kategorie] += 1
#     #print vek / 10
# print res

## tmp
# for p in Pacient.objects.all():
#     if not p.datum_transplantace:
#         continue
#     if p.diagnozy.count() > 1:
#         print p
#         for d in p.diagnozy.all():
#             print d

# dg = {
# 'Hemolytické anémie': ('D589', 'D591'),
# 'Aplastická anémie': ('D613', 'C619'),
# 'Idiopatická trombocytopenická purpura': ('D693',),
# 'Myelodysplastické syndromy': ('D462', 'D467', 'D469'),
# 'Akutní myeloidní leukémie': ('C920', 'C924'),
# 'Akutní lymfoblastická leukémie':  ('C910',),
# 'Akutní leukémie, nediferencovaná': ('C959',),
# 'Chronická lymfocytární leukémie': ('C911',),
# 'Mnohočetný myelom a plasmocytární novotvary': ('C900', 'C901'),
# 'Hodgkinova nemoc': ('C811', 'C812', 'C813'),
# 'Nehodgkinův folikulární  lymfom': ('C820', 'C827', 'C829'),
# 'Nehodgkinův difúzní  lymfom': ('C830', 'C831', 'C833', 'C837'),
# 'Periferní a kožní T-buněčné lymfomy': ('C840', 'C844', 'C845'),
# }
#
# dd = {}
# for k, v in dg.items():
#     for vv in v:
#         dd[vv] = k
#
# res = {}
# count = 0
# for p in Pacient.objects.all():
#     if not p.datum_transplantace:
#         continue
#     use = False
#     for o in p.odber_set.all():
#         if o.datum > p.datum_transplantace:
#             use = True
#     if not use:
#         print 'skipping', p
#         continue
#     count += 1
#     for d in p.diagnozy.all():
#         tmp = d.kod.upper()
#         try:
#             jmeno = dd[tmp]
#         except KeyError:
#             jmeno = 'Jiná'
#             print tmp, jmeno, p
#         if 'myelom a plasm' in jmeno:
#             print 'Myelom:', p
#         try:
#             res[jmeno] += 1
#         except KeyError:
#             res[jmeno] = 1
#
# for k, v in res.items():
#     print '%s;%s;' % (k, v)


# kody = {}
# for p in Pacient.objects.all():
#     if not p.datum_transplantace:
#         continue
#     use = False
#     for o in p.odber_set.all():
#         if o.datum > p.datum_transplantace:
#             use = True
#     if not use:
#         print 'skipping', p
#         continue
#     for d in p.diagnozy.all():
#         tmp = d.kod.upper()
#         try:
#             kody[tmp] += 1
#         except KeyError:
#             kody[tmp] = 1
#         print tmp, p
#
# print kody

# prukazy = Prukaz.objects.values_list('jmeno', flat=True).distinct()
# from django.db.models import F
#
# for prukaz in prukazy:
#     p = Prukaz.objects.filter(jmeno=prukaz)
#     tmp = VysledekTestu.objects.filter(prukaz__in=p)
#     tmp = tmp.filter(odber__pacient__datum_transplantace__isnull=False)
#     tmp = tmp.filter(odber__pacient__datum_transplantace__lte=F('odber__datum'))
#     odbery = {}
#     if tmp.odber in odbery:
#         continue
#     odbery.add(tmp.odber)
#     print prukaz, tmp.count()
#     poz = tmp.filter(vysledek='poz').count()
#     neg = tmp.filter(vysledek='neg').count()
#     x = tmp.filter(vysledek='x').count()
#     sz = tmp.filter(vysledek='sz').count()
#     hran = tmp.filter(vysledek='hran').count()
#     nehod = tmp.filter(vysledek='nehod').count()
#     print '%s;%s;%s;%s;%s;%s;%s' % (prukaz, poz, neg, x, sz, hran, nehod)

# from django.db.models import Count, F
# res = {}
# vys = VysledekTestu.objects.filter(vysledek='poz', odber__pacient__datum_transplantace__isnull=False, odber__pacient__datum_transplantace__lte=F('odber__datum'))
# print vys.count()
# odbery = set()
# for v in vys:
#     if v.odber in odbery:
#         continue
#     odbery.add(v.odber)
#     jmeno = v.prukaz.jmeno
#     print jmeno
    
#
# from django.db.models import Count, F
# viry = Prukaz.objects.filter(typ='v')
# tmp = VysledekTestu.objects.filter(prukaz__in=viry, vysledek='neg')
# tmp = tmp.filter(odber__pacient__datum_transplantace__isnull=False)
# tmp = tmp.filter(odber__pacient__datum_transplantace__lte=F('odber__datum'))
# poz_viry = tmp.order_by().values('prukaz__jmeno').annotate(count=Count('prukaz__jmeno'))
# for x in poz_viry:
#     print '%s: %s' % (x['prukaz__jmeno'], x['count'])

count = 0
for o in Odber.objects.all().order_by('datum'):
    if not o.pacient.datum_transplantace or o.pacient.datum_transplantace > o.datum:
        continue
    prukazy = o.vysledky.filter(prukaz__typ='v')
#    prukazy = o.vysledky.filter(prukaz__typ='v').exclude(vysledek='x')
#    vys = prukazy.exclude(Q(vysledek='poz')|Q(vysledek='sz'))
    print o, ','.join([str(x) for x in prukazy if x.vysledek in ['poz', 'sz']])
    count += 1
#     if prukazy.count() != prukazy.filter(vysledek='neg'):
#         print o
#     if prukazy.count() == o.vysledky.filter(prukaz__typ='v').exclude(vysledek='poz').count():
#         print o.vysledky.all()
print count

# viry = Prukaz.objects.filter(typ='v')
# tmp = VysledekTestu.objects.filter(prukaz__in=viry, vysledek='neg')
# tmp = tmp.filter(odber__pacient__datum_transplantace__isnull=False)
# tmp = tmp.filter(odber__pacient__datum_transplantace__lte=F('odber__datum'))
# tmp = tmp.filter(prukaz__jmeno='RSV').order_by('odber')
# for x in tmp:
#     print x
# poz_viry = tmp.order_by().values('prukaz__jmeno').annotate(count=Count('prukaz__jmeno'))
# for x in poz_viry:
#     print '%s: %s' % (x['prukaz__jmeno'], x['count'])



## Koinfekce - verze 1
# viry = Prukaz.objects.filter(typ='v')
# bakterie = Prukaz.objects.filter(typ='b')
# houby = Prukaz.objects.filter(typ='h')
# res = {}
# def do_add(k):
#     try:
#         res[k] += 1
#     except KeyError:
#         res[k] = 1
# count = 0
# for odber in Odber.objects.all():
#     if odber.pacient.datum_transplantace is None or odber.pacient.datum_transplantace > odber.datum:
#         continue
#     count += 1
#     vys = VysledekTestu.objects.filter(odber=odber)
#     v_ = vys.filter(prukaz__in=viry, vysledek='poz').count()
#     b_ = vys.filter(prukaz__in=bakterie, vysledek='poz').count()
#     h_ = vys.filter(prukaz__in=houby, vysledek='poz').count()
#     if v_ and b_ and h_:
#         do_add('v+b+h')
#     elif v_ and b_:
#         do_add('v+b')
#     elif b_ and h_:
#         do_add('b+h')
#     elif v_ and h_:
#         do_add('v+h')
#     elif v_:
#         do_add('v')
#     elif b_:
#         do_add('b')
#     elif h_:
#         do_add('h')
#     else:
#         do_add('nic')
#
# print count
# print res


#
# from django.db.models import F
# for prukaz in Prukaz.objects.all():
#     jmeno = str(prukaz)
#     tmp = VysledekTestu.objects.filter(prukaz=prukaz)
#     tmp = tmp.filter(odber__pacient__datum_transplantace__isnull=False)
#     tmp = tmp.filter(odber__pacient__datum_transplantace__lte=F('odber__datum'))
#     poz = tmp.filter(vysledek='poz').count()
#     neg = tmp.filter(vysledek='neg').count()
#     x = tmp.filter(vysledek='x').count()
#     sz = tmp.filter(vysledek='sz').count()
#     hran = tmp.filter(vysledek='hran').count()
#     nehod = tmp.filter(vysledek='nehod').count()
#     print '%s;%s;%s;%s;%s;%s;%s' % (jmeno, poz, neg, x, sz, hran, nehod)

# agens = {}
# for jmeno in Agens.objects.all().values_list('jmeno', flat=True):
#     agens[jmeno] = 0
#
# for odber in Odber.objects.all().order_by('pacient'):
#     if odber.pacient.datum_transplantace is None or odber.pacient.datum_transplantace > odber.datum:
#         continue
#     tmp = set()
#     for v in odber.vysledky.filter(vysledek='poz'):
#         print v.odber.pacient.rc, v.odber.datum, v.prukaz.agens
#         tmp.add(v.prukaz.agens.jmeno)
#     while tmp:
#         agens[tmp.pop()] += 1
# #     print tmp
#     print '---'
#
# for jmeno in Agens.objects.all().values_list('jmeno', flat=True):
#     print jmeno, agens[jmeno]
