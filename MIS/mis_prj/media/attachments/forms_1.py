from django import forms
from .models import TrainedPeople,EmployeeData

class PeopleTrainedForm(forms.ModelForm):
    class Meta:
        model = TrainedPeople
        fields = ['onroll_male', 'onroll_female', 'offroll_male', 'offroll_female']
        labels = {
            'onroll_male': 'Onroll - Male',
            'onroll_female': 'Onroll - Female',
            'offroll_male': 'Off roll - Male',
            'offroll_female': 'Off roll - Female',
        }

class ManhoursForm(forms.ModelForm):
    class Meta:
        model = TrainedPeople
        fields = ['onroll_male', 'onroll_female', 'offroll_male', 'offroll_female']
        labels = {
            'onroll_male': 'Onroll - Male',
            'onroll_female': 'Onroll - Female',
            'offroll_male': 'Off roll - Male',
            'offroll_female': 'Off roll - Female',
        }

class EmployeeDataForm(forms.ModelForm):
    class Meta:
        model = EmployeeData
        fields = ['division', 'location', 'department']