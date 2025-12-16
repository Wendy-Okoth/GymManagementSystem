from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ⭐") for i in range(1, 6)]),
            'comment': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Write your feedback here...',
                    'class': 'form-control'
                }
            ),
        }



