from django import forms
from django.forms import ModelForm

from members.models import Member, SUBSCRIPTION_PERIOD_CHOICES, SUBSCRIPTION_TYPE_CHOICES, FEE_STATUS, BATCH, STATUS, \
    Manager


class AddMemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].error_messages = {'required': 'Please enter the first name'}
        self.fields['last_name'].error_messages = {'required': 'Please enter the last name'}

    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user', 'registration_upto']
        widgets = {
            'registration_date': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'medical_history': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'dob': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*;capture=camera'})
        }

    def clean_mobile_number(self, *args, **kwargs):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit():
            raise forms.ValidationError('Mobile number should be a number')
        if Member.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError('This mobile number has already been registered.')
        else:
            if len(str(mobile_number)) == 10:
                return mobile_number
            else:
                raise forms.ValidationError('Mobile number should be 10 digits long.')



    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        first_name = cleaned_data.get('first_name').capitalize()
        last_name = cleaned_data.get('last_name').capitalize()
        queryset = Member.objects.filter(
            first_name=first_name,
            last_name=last_name,
            dob=dob
        ).count()
        if queryset > 0:
            raise forms.ValidationError('This member already exists!')


class SearchForm(forms.Form):
    search = forms.CharField(label='Search Member', max_length=100, required=False)

    def clean_search(self, *args, **kwargs):
        search = self.cleaned_data.get('search')
        if search == '':
            raise forms.ValidationError('Please enter a name in search box')
        return search


class UpdateMemberGymForm(forms.Form):
    registration_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker        form-control', 'type': 'date'}), )
    registration_upto = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}), )
    subscription_type = forms.ChoiceField(choices=SUBSCRIPTION_TYPE_CHOICES)
    subscription_period = forms.ChoiceField(choices=SUBSCRIPTION_PERIOD_CHOICES)
    fee_status = forms.ChoiceField(choices=FEE_STATUS)
    batch = forms.ChoiceField(choices=BATCH)
    stop = forms.ChoiceField(label='Status', choices=STATUS)



class UpdateMemberInfoForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    photo = forms.FileField(label='Update Photo', required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}), )


class AddManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['manager_name', 'manager_email', 'manager_phone', 'manager_address', 'dob', 'photo']
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*;capture=camera'})
        }

    def clean_manager_email(self):
        manager_email = self.cleaned_data.get('manager_email')
        if Manager.objects.filter(manager_email=manager_email).exists():
            raise forms.ValidationError('This manager email has already been registered.')
        return manager_email
