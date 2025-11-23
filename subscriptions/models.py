from django.db import models
from datetime import timedelta, date

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('BI_ANNUAL', 'Bi-Annual'),
        ('ANNUAL', 'Annual'),
    ]

    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.plan_type} - {self.price} KES"

    def calculate_end_date(self, start_date):
        """Return expiry date based on plan type"""
        if self.plan_type == 'DAILY':
            return start_date + timedelta(days=1)
        elif self.plan_type == 'WEEKLY':
            return start_date + timedelta(days=7)
        elif self.plan_type == 'MONTHLY':
            return start_date + timedelta(days=30)
        elif self.plan_type == 'BI_ANNUAL':
            return start_date + timedelta(days=180)  # ~6 months
        elif self.plan_type == 'ANNUAL':
            return start_date + timedelta(days=365)
        return start_date

