
from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'price', 'duration_days')
    list_filter = ('plan_type',)
    search_fields = ('plan_type',)
