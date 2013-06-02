from django.db import models
from django.utils import simplejson

class Pacient(models.Model):
    rc = models.CharField(max_length=11)
    jmeno = models.CharField(max_length=30)
    prijmeni = models.CharField(max_length=30)
    json_data = models.TextField()

    def __unicode__(self):
        return '%s, %s [%s]' % (self.prijmeni[:4], self.jmeno[:2], self.rc[:2])

    def sparkline_data(self):
        return [x[1] for x in simplejson.loads(self.json_data)]
