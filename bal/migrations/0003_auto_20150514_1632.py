# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0002_auto_20150514_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='BAL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField()),
                ('exitus', models.BooleanField(default=False)),
                ('agranulocytoza', models.BooleanField(default=False)),
                ('alogenni_transplantace', models.BooleanField(default=False)),
                ('pacient', models.ForeignKey(to='bal.Pacient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='odber',
            options={},
        ),
        migrations.RemoveField(
            model_name='odber',
            name='datum',
        ),
        migrations.RemoveField(
            model_name='odber',
            name='pacient',
        ),
        migrations.AddField(
            model_name='odber',
            name='bal',
            field=models.ForeignKey(related_name='odbery', default='', to='bal.BAL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='odber',
            name='kultivace_memo',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='odber',
            name='kultivace_typ',
            field=models.CharField(blank=True, max_length=1, choices=[(b'P', b'Primokultura'), (b'X', b'Po pomnozeni')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='odber',
            name='kultivace_vysledek',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='odber',
            name='nalez',
            field=models.ForeignKey(related_name='odbery', default='', to='bal.Agens'),
            preserve_default=False,
        ),
    ]
