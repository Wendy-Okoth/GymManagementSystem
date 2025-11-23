from django.contrib import admin
from .models import Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'gender', 'date_of_birth', 'age')
    list_filter = ('specialization', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
