"""
Tests for Service Plans app
"""
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from service_plans.models import ServiceSubscription, ServiceSubscriptionHistory


class ServiceSubscriptionTest(TestCase):
    """
    Tests for basic service subscription functionality
    """
    @override_settings(
        REGISTRATION_EXTRA_FIELDS={
            key: "optional"
            for key in ["level_of_education", "gender", "mailing_address", "city", "country",
                        "goals", "year_of_birth", "honor_code"]
        }
    )
    def test_service_subscription_created_on_account_creation(self):
        """
        Test survice subscription is created for newly registered user
        """
        username = 'test_user'
        url = reverse('create_account')
        response = self.client.post(url, {
            'username': username,
            'email': 'test@example.com',
            'password': 'test_password',
            'name': 'Test user',
            'terms_of_service': True,
        })
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            ServiceSubscription.objects.filter(user__username=username).exists(),
            "Service subscription is not created")

    def test_subscription_history_created_on_user_creation(self):
        """
        Test signals for service subscription and subscription history are emitted
        """
        user = User.objects.create(username='test')
        service_subscription = ServiceSubscription.objects.get(user=user)
        self.assertEqual(service_subscription.history.count(), 1)

    def test_subscription_history_created_on_subscription_change(self):
        """
        Test subscription history tracks every service subscription change
        """
        user = User.objects.create(username='test')
        service_subscription = ServiceSubscription.objects.get(user=user)
        service_subscription.is_premium = True
        service_subscription.save()

        self.assertEqual(service_subscription.history.count(), 2)
        self.assertEqual(service_subscription.history.latest().is_premium, True)

    def test_default_service_plan_on_user_creation(self):
        """
        Test default service plan is chosen for new user
        """
        user = User.objects.create(username='test')
        service_plan = ServiceSubscription.get_current_plan_for_user(user)

        self.assertEqual(service_plan.is_default, True)

    @override_settings(LANGUAGE_CODE='en')
    def test_non_default_service_plan(self):
        """
        Test that after setting 'is_premium' flag for user's service subscription
        user's service plan would be 'Premium', not a default one
        """
        user = User.objects.create(username='test')
        service_subscription = ServiceSubscription.objects.get(user=user)
        service_subscription.is_premium = True
        service_subscription.save()

        service_plan = ServiceSubscription.get_current_plan_for_user(user)
        self.assertFalse(service_plan.is_default)
        self.assertEqual(unicode(service_plan.name), 'Premium')
