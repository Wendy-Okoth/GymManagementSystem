
from django.db import models
from members.models import Member
from instructors.models import Instructor
from attendance.models import Attendance   

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 stars

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True, blank=True)

    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    thumbs_up = models.BooleanField(null=True, blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.member} for {self.instructor} ({self.attendance})"
