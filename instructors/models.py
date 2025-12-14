from django.db import models
from datetime import date
from django.contrib.auth.hashers import make_password, check_password

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

    # ✅ New field for login
    password = models.CharField(max_length=128, null=True, blank=True)

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

    # ✅ Helpers for password management
    def set_password(self, raw_password):
        """Hash and set the instructor's password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify a raw password against the stored hash."""
        return check_password(raw_password, self.password)

