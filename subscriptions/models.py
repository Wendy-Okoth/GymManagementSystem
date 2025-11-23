from django.db import models

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
    duration_days = models.PositiveIntegerField()  # e.g. 1, 7, 30, 180, 365

    def __str__(self):
        return f"{self.plan_type} - {self.price} KES"

