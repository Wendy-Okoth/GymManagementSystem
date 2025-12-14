from django.contrib import admin
from .models import Instructor
from .forms import InstructorAdminForm

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    form = InstructorAdminForm  # ✅ use custom form for password hashing

    list_display = (
        'first_name', 'last_name', 'email', 'phone_number',
        'specialization', 'gender', 'date_of_birth', 'age'
    )
    list_filter = ('specialization', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ('last_name', 'first_name')


