from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'price', 'duration_display')
    list_filter = ('plan_type',)
    search_fields = ('plan_type',)

    def duration_display(self, obj):
        if obj.plan_type == 'DAILY':
            return "1 day"
        elif obj.plan_type == 'WEEKLY':
            return "7 days"
        elif obj.plan_type == 'MONTHLY':
            return "30 days"
        elif obj.plan_type == 'BI_ANNUAL':
            return "6 months"
        elif obj.plan_type == 'ANNUAL':
            return "365 days"
        return "-"
    duration_display.short_description = "Duration"


