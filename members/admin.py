
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'date_of_birth', 'age',
        'workout_time', 'subscription_plan', 'gym_instructor'
    )
    list_filter = ('gender', 'workout_time', 'subscription')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

    def subscription_plan(self, obj):
        if obj.subscription:
            return f"{obj.subscription.plan_type} - {obj.subscription.price} KES"
        return "No Subscription"
    subscription_plan.short_description = "Subscription"
