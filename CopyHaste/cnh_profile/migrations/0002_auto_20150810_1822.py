# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnh_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cnhprofile',
            name='website_url',
        ),
        migrations.AddField(
            model_name='cnhprofile',
            name='website',
            field=models.URLField(help_text=b'What is your website URL?', blank=True),
        ),
        migrations.AlterField(
            model_name='cnhprofile',
            name='nickname',
            field=models.CharField(help_text=b'What is your nickname', max_length=16, null=True, blank=True),
        ),
    ]
