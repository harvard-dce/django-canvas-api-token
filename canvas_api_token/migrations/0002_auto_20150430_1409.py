# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('canvas_api_token', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvasDeveloperKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consumer_key', models.CharField(unique=True, max_length=30)),
                ('client_id', models.CharField(max_length=30)),
                ('client_secret', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'canvas_dev_key',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='canvasapitoken',
            name='user_id',
        ),
        migrations.AddField(
            model_name='canvasapitoken',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
