from django import forms
from .models import Equipment


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100)


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_name', 'equipment_code', 'equipment_quantity', 'equipment_import_date',
                  'equipment_warranty_date', 'equipment_origin', 'equipment_status']