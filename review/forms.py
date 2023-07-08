from django import forms
from .models import Member

class addReviewForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=100)
    rating = forms.IntegerField()
    trainer = forms.CharField(label='Trainer', max_length=100)
    member = forms.ModelChoiceField(label='Member', queryset=Member.objects.all())
