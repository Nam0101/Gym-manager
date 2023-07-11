from django import forms

from members.models import Manager
from .models import Equipment
from .models import Room

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100)


class EquipmentForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Room')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['room'].widget = forms.HiddenInput()
            current_manager = Manager.objects.get(user=user)
            self.fields['room'].initial = current_manager.room

    class Meta:
        model = Equipment
        fields = ['equipment_name', 'equipment_code', 'room', 'equipment_import_date',
                  'equipment_warranty_date', 'equipment_origin', 'equipment_status']
        widgets = {
            'equipment_import_date': forms.DateInput(attrs={'type': 'date'}),
            'equipment_warranty_date': forms.DateInput(attrs={'type': 'date'}),
        }
