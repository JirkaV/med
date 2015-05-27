# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jmeno', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Agens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Diagnoza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kod', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Diagnozy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Odber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField(default=datetime.date(2015, 5, 14))),
            ],
            options={
                'verbose_name_plural': 'Odbery',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pacient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rc', models.CharField(max_length=11)),
                ('pohlavi', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Muz'), (b'Z', b'Zena')])),
                ('datum_narozeni', models.DateField(default=datetime.date(2015, 5, 14))),
                ('datum_transplantace', models.DateField(null=True, blank=True)),
                ('diagnozy', models.ManyToManyField(to='bal.Diagnoza', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Pacienti',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prukaz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jmeno', models.CharField(max_length=40)),
                ('metoda', models.CharField(default=b'PCR', max_length=10, choices=[(b'PCR', b'PCR Metody'), (b'chromat', b'Imunochromatografie - Ag'), (b'manan', b'Prukaz Asp mananu'), (b'bak_kul', b'Bakterialni kultivace'), (b'myk_kul', b'Mykologicka kultivace'), (b'imun', b'Imunologicky')])),
                ('typ', models.CharField(default=b'v', max_length=1, choices=[(b'v', b'virus'), (b'b', b'bakterie'), (b'h', b'houba'), (b'p', b'parazit')])),
                ('sloupec', models.IntegerField()),
                ('agens', models.ForeignKey(blank=True, to='bal.Agens', null=True)),
            ],
            options={
                'ordering': ['jmeno'],
                'verbose_name_plural': 'Prukazy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VysledekTestu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vysledek', models.CharField(max_length=10, choices=[(b'neg', b'Negativni'), (b'poz', b'Pozitivni'), (b'x', b'Nemereno'), (b'hran', b'Hranicni'), (b'sz', b'Seda zona'), (b'nehod', b'Nehodnotitelne')])),
                ('odber', models.ForeignKey(related_name='vysledky', to='bal.Odber')),
                ('prukaz', models.ForeignKey(related_name='vysledky', to='bal.Prukaz')),
            ],
            options={
                'verbose_name_plural': 'Vysledky odberu',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='odber',
            name='pacient',
            field=models.ForeignKey(to='bal.Pacient'),
            preserve_default=True,
        ),
    ]
