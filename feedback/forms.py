from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['attendance', 'rating', 'thumbs_up', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} ⭐") for i in range(1, 6)]),
            'thumbs_up': forms.CheckboxInput(),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your feedback...'}),
        }
