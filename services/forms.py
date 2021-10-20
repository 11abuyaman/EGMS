from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PeriodicMedication, Result


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'phone', 'gender', 'national_number', 'has_cancer', 'has_hypertension',
            'has_hyperlipidemia', 'has_diabetes'
        )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'phone', 'national_number', 'country', 'gender']


class EditPatientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'national_number', 'country', 'gender', 'has_diabetes',
                  'has_cancer', 'has_hypertension', 'has_hyperlipidemia', ]


class PeriodicMedicationForm(forms.ModelForm):
    class Meta:
        model = PeriodicMedication
        fields = ['start_date', 'end_date', 'patient', 'medicine', 'period']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['file', 'patient', 'remarks', 'medicines', 'result_by']
