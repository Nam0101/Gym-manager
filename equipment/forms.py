from django import forms
from .models import Equipment
from .models import room

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100)


class EquipmentForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=room.objects.all(), label='Room')

    class Meta:
        model = Equipment
        fields = ['equipment_name', 'equipment_code', 'room', 'equipment_import_date',
                  'equipment_warranty_date', 'equipment_origin', 'equipment_status']
        widgets = {
            'equipment_import_date': forms.DateInput(attrs={'type': 'date'}),
            'equipment_warranty_date': forms.DateInput(attrs={'type': 'date'}),
        }

