"""
Models related to Eduardo service plans functionality
"""
from collections import namedtuple, OrderedDict

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# Temporary object type for Service Plan, to be replaced with model
ServicePlan = namedtuple('ServicePlan',
                         ('name', 'description', 'monthly_price', 'yearly_price',
                          'currency', 'is_default', 'sequence_no'))
BASIC_SERVICE_PLAN = ServicePlan(
    name=_('Basic'),
    description=_('Free service plan'),
    monthly_price=0,
    yearly_price=0,
    currency='',
    is_default=True,
    sequence_no=1
)
PREMIUM_SERVICE_PLAN = ServicePlan(
    name=_('Premium'),
    description=_('Paid service plan'),
    monthly_price=0,  # dummy price values
    yearly_price=0,
    currency='',
    is_default=False,
    sequence_no=2
)


class ServiceSubscription(models.Model):
    """
    Model for storing user's service plan and corresponding attributes.
    """
    class Meta:
        app_label = 'service_plans'
        verbose_name = _('service subscription')
        verbose_name_plural = _('service subscriptions')

    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE, db_index=True)
    expires = models.DateField(verbose_name=_('expires'), default=None, null=True, blank=True)
    comment = models.TextField(verbose_name=_('comment'), default='', blank=True)

    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('modified'), auto_now=True)

    # Temporary field to be replaced with ServicePlan foreign key
    is_premium = models.BooleanField(verbose_name=_('premium'), default=False, db_index=True)

    def _get_service_plan(self):
        """Helper method for temporary service plan selection"""
        if self.is_premium:
            return PREMIUM_SERVICE_PLAN
        else:
            return BASIC_SERVICE_PLAN

    def __unicode__(self):
        return u'<ServiceSubscription for {user.username}: {plan.name}>'.format(
            user=self.user, plan=self._get_service_plan())

    @classmethod
    def get_current_plan_for_user(cls, user):
        """
        Recommended way of getting service plan currently enabled for user
        """
        service_subscription, _ = cls.objects.get_or_create(user=user)
        return service_subscription._get_service_plan()


@receiver(post_save, sender=User)
def create_service_subscription(sender, instance, created, **kwargs):
    """
    Create service subscription on user creation
    Skip signals on "raw" creations during test database fixture loading
    """
    if created and not kwargs.get('raw', False):
        ServiceSubscription.objects.create(user=instance)


class ServiceSubscriptionHistory(models.Model):
    """
    Keeps a complete history of service subscription changes for a user.
    """
    class Meta:
        app_label = 'service_plans'
        verbose_name = _('service subscription history item')
        verbose_name_plural = _('service subscription history')
        get_latest_by = 'created'
        ordering = ('-created',)

    service_subscription = models.ForeignKey(
        ServiceSubscription, verbose_name=_('service subscription'),
        related_name='history', on_delete=models.CASCADE, db_index=True)

    # Fields populated from corresponding ServiceSubscription
    expires = models.DateField(verbose_name=_('expires'), null=True, blank=True)
    comment = models.TextField(verbose_name=_('comment'), blank=True)

    # History creation timestamp populated from ServiceSubscription modification timestamp
    created = models.DateTimeField(verbose_name=_('created'), db_index=True)

    # Temporary field to be replaced with ServicePlan foreign key
    is_premium = models.BooleanField(verbose_name=_('premium'))

    @receiver(post_save, sender=ServiceSubscription)
    def save_history(sender, instance, **kwargs):  # pylink: disable=no-self-argument, unused-argument
        ServiceSubscriptionHistory.objects.create(
            service_subscription=instance,
            created=instance.modified,
            expires=instance.expires,
            comment=instance.comment,
            is_premium=instance.is_premium)
