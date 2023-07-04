from django.db import models
from django.forms import ModelForm
from django import forms

STATUS_CHOICES = [
    ('available', 'Available'),
    ('in use', 'In Use'),
    ('maintenance', 'Maintenance'),
    ('repair', 'Repair'),
    ('out of order', 'Out of Order'),
]


# Create your models here.
class Equipment(models.Model):
    equipment_name = models.CharField('Name', max_length=50)
    equipment_code = models.CharField('Code', max_length=50, unique=True)
    equipment_quantity = models.IntegerField('Quantity')
    equipment_import_date = models.DateField('Import Date')
    equipment_warranty_date = models.DateField('Warranty Date')
    equipment_origin = models.CharField('Origin', max_length=50)
    equipment_status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['equipment_name']


class AddEquipmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['equipment_name'].error_messages = {'required': 'Please enter equipment name'}
        self.fields['equipment_code'].error_messages = {'required': 'Please enter equipment code'}
        self.fields['equipment_quantity'].error_messages = {'required': 'Please enter equipment quantity'}
        self.fields['equipment_import_date'].error_messages = {'required': 'Please enter equipment import date'}
        self.fields['equipment_warranty_date'].error_messages = {'required': 'Please enter equipment warranty date'}
        self.fields['equipment_origin'].error_messages = {'required': 'Please enter equipment origin'}

        class Meta:
            model = Equipment
            fields = '__all__'
            exclude = ['equipment_status']
            widgets = {
                'equipment_import_date': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
                'equipment_warranty_date': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
            }


class UpdateEquipmentForm(forms.Form):
    equipment_name = forms.CharField(label='Name', max_length=50)
    equipment_code = forms.CharField(label='Code', max_length=50)
    equipment_quantity = forms.IntegerField(label='Quantity')
    equipment_import_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}), label='Import Date')
    equipment_warranty_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}), label='Warranty Date')

    equipment_origin = forms.CharField(label='Origin', max_length=50)
    equipment_status = forms.CharField(label='Status', max_length=50)
