from django.db import models

class ReferenceDNA(models.Model):
    name = models.CharField(max_length=40)
    dna = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
