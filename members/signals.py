from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from datetime import date, timedelta
from .models import Member

# Map subscription plans to durations
PLAN_DURATIONS = {
    "DAILY": timedelta(days=1),
    "WEEKLY": timedelta(weeks=1),
    "MONTHLY": timedelta(days=30),
    "BIANNUAL": timedelta(days=182),  # approx 6 months
    "YEARLY": timedelta(days=365),
}

@receiver(post_save, sender=Member)
def send_expiry_reminder(sender, instance, **kwargs):
    # Only check if member has a plan and has paid
    if instance.subscription_plan and instance.has_paid:
        duration = PLAN_DURATIONS.get(instance.subscription_plan)
        if duration:
            expiry_date = instance.join_date + duration
            if date.today() > expiry_date:
                send_mail(
                    subject="Your Gym Subscription Has Expired",
                    message=(
                        f"Hi {instance.first_name},\n\n"
                        f"Your {instance.subscription_plan} plan expired on {expiry_date}.\n"
                        "Please renew to continue enjoying our gym services."
                    ),
                    from_email="gymencorewebsite@gmail.com",
                    recipient_list=[instance.email],
                    fail_silently=True,  # avoids crashing if email fails
                )

