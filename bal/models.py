import datetime
from django.db import models
from .utils import rc2datum

POHLAVI = (
  ('M', 'Muz'),
  ('Z', 'Zena'),
)

METODY = (
    ('PCR', 'PCR Metody'),
    ('chromat', 'Imunochromatografie - Ag'),
    ('manan', 'Prukaz Asp mananu'),
    ('bak_kul', 'Bakterialni kultivace'),
    ('myk_kul', 'Mykologicka kultivace'),
    ('imun', 'Imunologicky'),
)

TYPY = (
    ('v', 'virus'),
    ('b', 'bakterie'),
    ('h', 'houba'),
    ('p', 'parazit'),
)

KULTIVACE = (
    ('P', 'Primokultura'),
    ('X', 'Po pomnozeni'),
)

VYSLEDKY = (
  ('neg', 'Negativni'),
  ('poz', 'Pozitivni'),
  ('x', 'Nemereno'),
  ('hran', 'Hranicni'),
  ('sz', 'Seda zona'),
  ('nehod', 'Nehodnotitelne')
)

class Diagnoza(models.Model):
    '''diagnoza'''
    kod = models.CharField(max_length=512)
    
    class Meta:
        verbose_name_plural = 'Diagnozy'

    def save(self, *args, **kwargs):
        self.kod = self.kod.upper()
        super(Diagnoza, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.kod
    
class Pacient(models.Model):
    '''pacient'''
    rc = models.CharField(max_length=11)
    pohlavi = models.CharField(max_length=1, choices=POHLAVI, blank=True)
    diagnozy = models.ManyToManyField(Diagnoza, blank=True, null=True)
    dg = models.ForeignKey(Diagnoza, blank=True, null=True, related_name='pacienti')
    datum_narozeni = models.DateField(default=datetime.date.today)
    datum_transplantace = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Pacienti'

    def save(self, *args, **kwargs):
        if not self.pohlavi:
            try:
                tmp = self.rc[2]
            except IndexError:
                raise ValueError, '[!] Chybne RC: %s' % self.rc
            if tmp in ['0', '1']:
                self.pohlavi = 'M'
            elif tmp in ['5', '6']:
                self.pohlavi = 'Z'
            else:
                raise ValueError, '[!] Chybne RC: %s' % self.rc

        d = rc2datum(self.rc)
        if d.year > 2000:
            tmp = datetime.date(year=d.year-100, month=d.month, day=d.day)
            d = tmp
        self.datum_narozeni = d
        super(Pacient, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.datum_transplantace is None:
            return self.rc
        else:
            return '%s [transplantovan %s]' % (self.rc, self.datum_transplantace)

class BAL(models.Model):
    datum = models.DateField()
    pacient = models.ForeignKey(Pacient, related_name='baly')

    exitus = models.BooleanField(default=False)
    agranulocytoza = models.NullBooleanField(blank=True, null=True, default=False)
    alogenni_transplantace = models.NullBooleanField(blank=True, null=True, default=False)

    def __unicode__(self):
        return 'BAL %s z %s' % (self.pacient.rc, self.datum)

class Agens(models.Model):
    '''skupina prukazu / nalez'''
    jmeno = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Agens'

    def __unicode__(self):
        return self.jmeno

class Odber(models.Model):
    '''odber konkretnimu pacientovi'''
    bal = models.ForeignKey(BAL, related_name='odbery')
    nalez = models.ForeignKey(Agens, related_name='odbery')
    kultivace_typ = models.CharField(max_length=1, choices=KULTIVACE, blank=True)
    kultivace_vysledek = models.CharField(max_length=100, blank=True)
    kultivace_memo = models.CharField(max_length=200, blank=True)

class Prukaz(models.Model):
    '''test na konkretni virus/bakterii/houbu'''
    jmeno = models.CharField(max_length=40)
    metoda = models.CharField(max_length=10, choices=METODY, default='PCR')
    typ = models.CharField(max_length=1, choices=TYPY, default='v')
    agens = models.ForeignKey(Agens, blank=True, null=True)
    sloupec = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Prukazy'
        ordering = ['jmeno']

    def __unicode__(self):
        return '%s [%s]' % (self.jmeno, self.get_metoda_display())

class VysledekTestu(models.Model):
    '''vysledek jednoho testu'''
    odber = models.ForeignKey(Odber, related_name='vysledky')
    prukaz = models.ForeignKey(Prukaz, related_name='vysledky')
    vysledek = models.CharField(max_length=10, choices=VYSLEDKY)

    class Meta:
        verbose_name_plural = 'Vysledky odberu'

    def __unicode__(self):
        return '%s u %s [%s]: %s' % (self.prukaz.jmeno,
                                     self.odber.pacient,
                                     self.odber.datum,
                                     self.get_vysledek_display())
