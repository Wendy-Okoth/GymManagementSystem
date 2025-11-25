from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from datetime import date
from .models import Member

@receiver(post_save, sender=Member)
def send_expiry_reminder(sender, instance, **kwargs):
    if instance.subscription:
        expiry_date = instance.subscription.calculate_end_date(instance.join_date)
        if date.today() > expiry_date:
            send_mail(
                subject="Your Gym Subscription Has Expired",
                message=(
                    f"Hi {instance.first_name},\n\n"
                    f"Your {instance.subscription.plan_type} plan expired on {expiry_date}.\n"
                    "Please renew to continue enjoying our gym services."
                ),
                from_email="gymencorewebsite@gmail.com",
                recipient_list=[instance.email],
                fail_silently=True,  # avoids crashing if email fails
            )
