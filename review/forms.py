import datetime

from django import forms
from django.http import request

from trainers.models import Trainer
from .models import Member, Review
from django.contrib.auth.decorators import login_required


class addReviewForm(forms.Form):
    description = forms.CharField(label='description', max_length=100)
    rating = forms.ChoiceField(label='rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def save(self, request):
        current_user = request.user
        data = self.cleaned_data
        review = Review.objects.create(
            review_content=data['description'],
            review_star=data['rating'],
            review_date=datetime.date.today(),
            member=Member.objects.get(user=current_user)
        )
        return review
