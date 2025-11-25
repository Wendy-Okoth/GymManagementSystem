from django.db import models
from instructors.models import Instructor 
from datetime import date 

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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)

    workout_time = models.CharField(max_length=10, choices=WORKOUT_TIMES)
    gym_instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Calculate age dynamically from date_of_birth"""
        from datetime import date
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def is_subscription_active(self):
        if self.subscription:
            end_date = self.subscription.calculate_end_date(self.join_date)
            return date.today() <= end_date
        return False
