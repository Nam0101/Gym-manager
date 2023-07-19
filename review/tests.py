from datetime import date

from django.test import TestCase
from django.core.management import execute_from_command_line
from .models import Review


# Create your tests here.

# Path: review\tests.py
# Compare this snippet from members\forms.py:
# from django import forms
# from django.forms import ModelForm
class addReviewTest(TestCase):

    def setUp(self) -> None:
        self.review = Review.objects.create(
            review_content='test',
            review_date=date.today(),
            review_star=5,
        )

    def test_review(self):
        self.assertEqual(self.review.review_content, 'test')
        self.assertEqual(self.review.review_date, date.today())
        self.assertEqual(self.review.review_star, 5)


