from django.db import models

# Create your models here.
from django.db import models

class Member(models.Model):
    WORKOUT_TIMES = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
        ('NIGHT', 'Night'),
    ]

    MEMBERSHIP_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('BI_ANNUAL', 'Bi-Annual'),
        ('ANNUAL', 'Annual'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    join_date = models.DateField(auto_now_add=True)

    workout_time = models.CharField(max_length=10, choices=WORKOUT_TIMES)
    gym_instructor = models.CharField(max_length=100)
    membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

