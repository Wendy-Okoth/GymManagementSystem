from django.db import models
from django.core.exceptions import ValidationError
from members.models import Member
from instructors.models import Instructor
from datetime import date

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_time = models.DateTimeField(auto_now_add=True)
    workout_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        # ✅ Validate subscription before saving
        if self.member.subscription:
            start_date = self.member.join_date
            end_date = self.member.subscription.calculate_end_date(start_date)
            if date.today() > end_date:
                raise ValidationError("Member's subscription has expired. Cannot record attendance.")
        else:
            raise ValidationError("Member does not have an active subscription.")
        super().save(*args, **kwargs)
