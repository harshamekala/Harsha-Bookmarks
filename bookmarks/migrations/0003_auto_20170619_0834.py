# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 08:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmarks', '0002_friendship'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('from_friend', 'to_friend')]),
        ),
    ]