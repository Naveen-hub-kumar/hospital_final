from django import forms
from django.contrib.auth.models import User
from .models import Patient

class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['age', 'phone', 'address', 'gender','username', 'password']