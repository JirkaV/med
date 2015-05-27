# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0005_auto_20150514_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bal',
            name='pacient',
            field=models.ForeignKey(related_name='baly', to='bal.Pacient'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnoza',
            name='kod',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pacient',
            name='datum_narozeni',
            field=models.DateField(default=datetime.date(2015, 5, 16)),
            preserve_default=True,
        ),
    ]
