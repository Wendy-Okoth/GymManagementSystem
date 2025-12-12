from django.contrib import admin
from .models import Member
import datetime  # ✅ Fix: import datetime

class SubscriptionStatusFilter(admin.SimpleListFilter):
    title = 'Subscription Status'
    parameter_name = 'subscription_status'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Active'),
            ('expired', 'Expired'),
        ]

    def queryset(self, request, queryset):
        today = datetime.date.today()
        if self.value() == 'active':
            return queryset.filter(has_paid=True).exclude(subscription_expiry__lt=today)
        if self.value() == 'expired':
            return queryset.filter(has_paid=True, subscription_expiry__lt=today)
        return queryset


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'phone_number',
        'gender', 'date_of_birth', 'age', 'workout_time',
        'subscription_plan_display', 'subscription_expiry', 'has_paid', 'gym_instructor'
    )
    list_filter = ('gender', 'workout_time', 'has_paid', SubscriptionStatusFilter)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

    def subscription_plan_display(self, obj):
        """Show the subscription plan if available."""
        return obj.subscription_plan or "No Subscription"
    subscription_plan_display.short_description = "Subscription Plan"

    def subscription_expiry(self, obj):
        """Show expiry date if stored, otherwise N/A."""
        return obj.subscription_expiry or "N/A"
    subscription_expiry.short_description = "Expiry Date"

    def changelist_view(self, request, extra_context=None):
        """Add summary counts to the admin list view."""
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
            today = datetime.date.today()
            extra_context = {
                'total_members': qs.count(),
                'paid_members': qs.filter(has_paid=True).count(),
                'unpaid_members': qs.filter(has_paid=False).count(),
                'active_members': qs.filter(has_paid=True).exclude(subscription_expiry__lt=today).count(),
                'expired_members': qs.filter(has_paid=True, subscription_expiry__lt=today).count(),
            }
            response.context_data.update(extra_context)
        except (AttributeError, KeyError):
            pass
        return response

