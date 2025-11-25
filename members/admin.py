from django.contrib import admin
from .models import Member

class SubscriptionStatusFilter(admin.SimpleListFilter):
    title = 'Subscription Status'
    parameter_name = 'subscription_status'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Active'),
            ('expired', 'Expired'),
        ]

    def queryset(self, request, queryset):
        from datetime import date
        if self.value() == 'active':
            return queryset.filter(subscription__isnull=False).filter(
                subscription__plan_type__isnull=False
            ).filter(
                # keep only members whose subscription is still valid
                id__in=[m.id for m in queryset if m.is_subscription_active()]
            )
        if self.value() == 'expired':
            return queryset.filter(subscription__isnull=False).filter(
                id__in=[m.id for m in queryset if not m.is_subscription_active()]
            )
        return queryset

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'date_of_birth', 'age',
        'workout_time', 'subscription_plan', 'subscription_expiry', 'gym_instructor'
    )
    list_filter = ('gender', 'workout_time', SubscriptionStatusFilter)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

    def subscription_plan(self, obj):
        if obj.subscription:
            return f"{obj.subscription.plan_type} - {obj.subscription.price} KES"
        return "No Subscription"
    subscription_plan.short_description = "Subscription"

    def subscription_expiry(self, obj):
        if obj.subscription:
            return obj.subscription.calculate_end_date(obj.join_date)
        return "N/A"
    subscription_expiry.short_description = "Expiry Date"
