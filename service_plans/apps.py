from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ServicePlansConfig(AppConfig):
    name = 'service_plans'
    verbose_name = _("Service Plans and Subscriptions")
