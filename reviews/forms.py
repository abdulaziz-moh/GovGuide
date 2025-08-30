from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError("Invalid rating. Must be 1-5 stars.")
        return rating