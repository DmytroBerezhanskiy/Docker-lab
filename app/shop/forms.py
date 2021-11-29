from django import forms
from .models import Reviews


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating', 'body']
        labels = {
            'body': "Your review",
            'rating': "Your rating",
        }
