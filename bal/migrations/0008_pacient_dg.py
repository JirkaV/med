# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bal', '0007_auto_20150516_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacient',
            name='dg',
            field=models.ForeignKey(related_name='pacienti', blank=True, to='bal.Diagnoza', null=True),
            preserve_default=True,
        ),
    ]
