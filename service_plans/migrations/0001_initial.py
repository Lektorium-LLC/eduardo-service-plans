# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expires', models.DateField(default=None, null=True, verbose_name='expires', blank=True)),
                ('comment', models.TextField(default=b'', verbose_name='comment', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_premium', models.BooleanField(default=False, db_index=True, verbose_name='premium')),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'service subscription',
                'verbose_name_plural': 'service subscriptions',
            },
        ),
        migrations.CreateModel(
            name='ServiceSubscriptionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expires', models.DateField(null=True, verbose_name='expires', blank=True)),
                ('comment', models.TextField(verbose_name='comment', blank=True)),
                ('created', models.DateTimeField(verbose_name='created', db_index=True)),
                ('is_premium', models.BooleanField(verbose_name='premium')),
                ('service_subscription', models.ForeignKey(verbose_name='service subscription',
                                                           to='service_plans.ServiceSubscription')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': 'service subscription history item',
                'verbose_name_plural': 'service subscription history items',
            },
        ),
    ]
