# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cnh_scores', '0002_auto_20150810_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userscores',
            name='user',
            field=models.ManyToManyField(related_name='scores', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='player1',
            field=models.ManyToManyField(related_name='player1', to='cnh_scores.UserScores', blank=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='player2',
            field=models.ManyToManyField(related_name='player2', to='cnh_scores.UserScores', blank=True),
        ),
    ]
