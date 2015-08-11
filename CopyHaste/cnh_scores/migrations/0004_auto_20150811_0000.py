# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnh_scores', '0003_auto_20150810_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userscores',
            name='user',
        ),
        migrations.AddField(
            model_name='userscores',
            name='user',
            field=models.ForeignKey(related_name='scores', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
