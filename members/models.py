from django.db import models
from instructors.models import Instructor
from datetime import date, timedelta

class Member(models.Model):
    WORKOUT_TIMES = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
        ('NIGHT', 'Night'),
    ]

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    SUBSCRIPTION_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('BIANNUAL', 'Bi-Annual'),
        ('YEARLY', 'Yearly'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)

    workout_time = models.CharField(max_length=10, choices=WORKOUT_TIMES)
    specialization = models.CharField(max_length=50, choices=Instructor.SPECIALIZATION_CHOICES, null=True, blank=True)
    gym_instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")

    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, null=True, blank=True)
    subscription_expiry = models.DateField(null=True, blank=True)   # ✅ new field
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def calculate_expiry(self):
        """Calculate expiry date based on plan and join_date."""
        if not self.subscription_plan or not self.has_paid:
            return None

        start = date.today()
        if self.subscription_plan == 'DAILY':
            return start + timedelta(days=1)
        elif self.subscription_plan == 'WEEKLY':
            return start + timedelta(days=7)
        elif self.subscription_plan == 'MONTHLY':
            return start + timedelta(days=30)
        elif self.subscription_plan == 'BIANNUAL':
            return start + timedelta(days=180)
        elif self.subscription_plan == 'YEARLY':
            return start + timedelta(days=365)
        return None

    def is_subscription_active(self):
        """Check if subscription is still valid."""
        if self.subscription_expiry:
            return self.subscription_expiry >= date.today()
        return False
