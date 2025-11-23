

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

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"{self.member} - {self.subscription} - {self.amount} KES"

    def save(self, *args, **kwargs):
       if self.subscription and self.amount != self.subscription.price:
        raise ValueError("Payment amount must match subscription price")
       super().save(*args, **kwargs)


