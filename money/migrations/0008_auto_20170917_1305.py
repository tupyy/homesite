# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0007_auto_20170917_1244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentmodel',
            old_name='nume',
            new_name='user',
        ),
        migrations.AddField(
            model_name='paymentmodel',
            name='comments',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
