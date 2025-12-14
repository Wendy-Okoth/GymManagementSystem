from django import forms
from django.contrib.auth.hashers import make_password
from .models import Instructor

class InstructorAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Set a raw password here. It will be stored securely (hashed)."
    )

    class Meta:
        model = Instructor
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'specialization', 'gender', 'date_of_birth', 'password'
        ]

    def clean_password(self):
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            return make_password(raw_password)  # ✅ hash before saving
        return self.instance.password
