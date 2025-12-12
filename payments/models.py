from django.db import models
from members.models import Member
from subscriptions.models import Subscription

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa'),
        ('CARD', 'Card'),
        ('BANK', 'Bank Transfer'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        sub_name = self.subscription.plan_type if self.subscription else "No Plan"
        return f"{self.member} - {sub_name} - {self.amount} KES"

    def save(self, *args, **kwargs):
        # ✅ Validate price consistency if subscription is linked
        if self.subscription and self.amount != self.subscription.price:
            raise ValueError("Payment amount must match subscription price")
        super().save(*args, **kwargs)



