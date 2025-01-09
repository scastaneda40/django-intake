from django import forms
from .models import Submission
from django.contrib.auth.models import User

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['name', 'email', 'reason', 'preferred_date', 'preferred_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            print(f"User Full Name: {user.get_full_name()}")  # Debug full name
            print(f"User Email: {user.email}")               # Debug email
            self.fields['name'].initial = user.get_full_name()  # Prepopulate with user's full name
            self.fields['email'].initial = user.email           # Prepopulate with user's email

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
