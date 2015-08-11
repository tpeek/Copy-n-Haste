# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserScores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score_date', models.DateField(auto_now_add=True)),
                ('cpm', models.IntegerField(default=0)),
                ('mistakes', models.IntegerField(default=0)),
                ('user', models.OneToOneField(related_name='scores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
