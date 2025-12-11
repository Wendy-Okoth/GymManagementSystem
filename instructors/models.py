from django.db import models
from datetime import date

class Instructor(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    SPECIALIZATION_CHOICES = [
        ('WEIGHTLIFTING', 'Weightlifting'),
        ('CARDIO', 'Cardiovascular Training'),
        ('YOGA', 'Yoga'),
        ('PILATES', 'Pilates'),
        ('HIIT', 'High Intensive Interval Training'),
        ('FUNCTIONAL', 'Functional Training'),
        ('GROUP', 'Group Fitness Classes'),
        ('BODYBUILDING', 'Bodybuilding'),
        ('POWERLIFTING', 'Powerlifting'),
        ('FLEXIBILITY', 'Flexibility'),
        ('ZUMBA', 'Zumba'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_specialization_display()}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
