from django.contrib import admin
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ServiceSubscription, ServiceSubscriptionHistory


class ServiceSubscriptionHistoryInline(admin.TabularInline):
    model = ServiceSubscriptionHistory
    verbose_name_plural = _('History')

    fields = ('created', 'is_premium', 'comment')
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False


class ServiceSubscriptionChangelistForm(forms.ModelForm):
    """
    Form for modification of ServiceSubscription in admin list view
    """
    class Meta:
        model = ServiceSubscription
        fields = ('is_premium', 'comment')
        widgets = {
            'comment': forms.TextInput(attrs={'size': 100})
        }


@admin.register(ServiceSubscription)
class ServiceSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'courses_count', 'is_premium', 'comment')
    list_editable = ('is_premium', 'comment')
    list_filter = ('is_premium',)
    list_select_related = ('user',)
    list_per_page = 20
    search_fields = ('user__username', 'user__email')

    fields = ('user', 'is_premium', 'comment')
    readonly_fields = ('user',)
    inlines = (ServiceSubscriptionHistoryInline,)

    def get_queryset(self, request):
        queryset = super(ServiceSubscriptionAdmin, self).get_queryset(request)
        queryset = queryset.annotate(courses_count=models.Count('user__owned_courses'))
        return queryset

    def courses_count(self, instance):
        return instance.courses_count
    courses_count.short_description = _("Courses count")
    courses_count.admin_order_field = 'courses_count'

    def email(self, instance):
        return instance.user.email
    email.admin_order_field = 'user__email'

    def get_changelist_form(self, request, **kwargs):
        return ServiceSubscriptionChangelistForm
