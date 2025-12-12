from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'subscription', 'amount', 'method', 'payment_date')
    list_filter = ('method', 'payment_date')
    search_fields = (
        'member__first_name', 'member__last_name',
        'member__email', 'subscription__plan_type'
    )

