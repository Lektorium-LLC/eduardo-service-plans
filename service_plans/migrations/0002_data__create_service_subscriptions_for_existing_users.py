# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    """Create basic ServiceSubscription as if user is just registered"""
    ServiceSubscription = apps.get_model('service_plans', 'ServiceSubscription')
    ServiceSubscriptionHistory = apps.get_model('service_plans', 'ServiceSubscriptionHistory')
    User = apps.get_model('auth', 'User')
    for user in User.objects.all():
        # ServiceSubscription history is not created for initial item
        service_subscription = ServiceSubscription.objects.create(user=user)
        ServiceSubscriptionHistory.objects.create(
            service_subscription=service_subscription,
            created=service_subscription.modified,
            expires=service_subscription.expires,
            comment=service_subscription.comment,
            is_premium=service_subscription.is_premium)


def backwards(apps, schema_editor):
    ServiceSubscription = apps.get_model('service_plans', 'ServiceSubscription')
    ServiceSubscription.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('service_plans', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
