# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cnh_scores', '0004_auto_20150811_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matches',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='matches',
            name='player2',
        ),
        migrations.AddField(
            model_name='matches',
            name='loser',
            field=models.ForeignKey(related_name='loser', default=None, to='cnh_scores.UserScores'),
        ),
        migrations.AddField(
            model_name='matches',
            name='winner',
            field=models.ForeignKey(related_name='winner', default=None, to='cnh_scores.UserScores'),
        ),
        migrations.AlterField(
            model_name='userscores',
            name='user',
            field=models.ForeignKey(related_name='scores', default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
