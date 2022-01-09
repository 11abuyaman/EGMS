from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PeriodicMedication, Result, Appointment


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'phone', 'gender', 'national_number', 'type', 'is_staff'
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


class EditStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'national_number', 'gender']


class PeriodicMedicationForm(forms.ModelForm):
    class Meta:
        model = PeriodicMedication
        fields = ['start_date', 'end_date', 'patient', 'medicine', 'period']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['file', 'patient', 'remarks', 'medicines', 'result_by']


class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(
        format='%Y-%m-%d %H:%M',
        attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Appointment
        fields = ['date', 'department', 'doctor']
