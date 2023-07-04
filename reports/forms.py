from django import forms

REPORT_CHOICES = (
    ('member', 'Member'),
    ('equipment', 'Equipment'),
)


class ReportForm(forms.Form):
    report_type = forms.ChoiceField(label='Report Type', choices=REPORT_CHOICES)
