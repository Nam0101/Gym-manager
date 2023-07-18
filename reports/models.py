import calendar
import datetime
from django import forms

from django.db import models
from django.forms import ModelForm

from members.models import Member

YEAR_CHOICES = []
for year in range(2016, (datetime.datetime.now().year + 5)):
    YEAR_CHOICES.append((year, year))

BATCH = (
    ('morning', 'Morning'),
    ('evening', 'Evening'),
    ('', 'All')
)
REPORT_CHOICES = (
    ('member', 'Member'),
    ('equipment', 'Equipment'),
    ('revenue', 'Revenue')
)
MONTHS_CHOICES = tuple(zip(range(1, 13), (calendar.month_name[i] for i in range(1, 13))))


# Create your models here.
class GenerateReports(models.Model):
    month = models.IntegerField(choices=MONTHS_CHOICES, default=datetime.datetime.now().year, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    batch = models.CharField(
        max_length=30,
        choices=BATCH,
        default=BATCH[2][0],
        blank=True)


class GenerateReportForm(ModelForm):
    report_type = forms.ChoiceField(label='Report Type', choices=REPORT_CHOICES)

    class Meta:
        model = GenerateReports
        fields = '__all__'
