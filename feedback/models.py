from django.db import models
from members.models import Member
from instructors.models import Instructor

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 stars

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    # ✅ Automatically stores the date feedback was created
    date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.member} for {self.instructor} on {self.date}"

