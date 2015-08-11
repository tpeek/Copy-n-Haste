# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnh_scores', '0005_auto_20150811_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userscores',
            name='cpm',
        ),
        migrations.AddField(
            model_name='userscores',
            name='wpm_gross',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userscores',
            name='wpm_net',
            field=models.IntegerField(default=0),
        ),
    ]
