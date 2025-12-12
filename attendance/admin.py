from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'instructor', 'check_in_time', 'workout_type')
    list_filter = ('instructor', 'workout_type')
    search_fields = (
        'member__first_name', 'member__last_name', 'member__email',
        'instructor__first_name', 'instructor__last_name', 'instructor__email'
    )

