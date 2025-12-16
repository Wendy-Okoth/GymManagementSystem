from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # ✅ Only include fields that exist on Feedback
    list_display = ('member', 'instructor', 'rating', 'comment', 'date', 'created_at')
    search_fields = ('member__email', 'instructor__name', 'comment')
    list_filter = ('date', 'rating')


