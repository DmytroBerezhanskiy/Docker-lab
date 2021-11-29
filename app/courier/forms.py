from django import forms
from courier.models import CouriersReview


class CouriersReviewForm(forms.ModelForm):
    class Meta:
        model = CouriersReview
        fields = ['rating', 'body']
        labels = {
            'body': "Your review",
            'rating': "Your rating",
        }
