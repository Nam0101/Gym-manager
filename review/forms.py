import datetime

from django import forms
from django.http import request

from trainers.models import Trainer
from .models import Member, Review
from django.contrib.auth.decorators import login_required


class addReviewForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=100)
    rating = forms.ChoiceField(label='Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    trainer = forms.ModelChoiceField(label='Trainer', queryset=Trainer.objects.all(), required=False)

    def save(self):
        current_user = request.user
        data = self.cleaned_data
        review = Review.objects.create(
            review_content=data['description'],
            review_star=data['rating'],
            review_date=datetime.date.today(),
            member=Member.objects.get(user=current_user)
        )
        return review
