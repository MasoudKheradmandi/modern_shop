from django import forms

from account.models import validate_phone_number

class LoginForm(forms.Form):
    phone_number = forms.CharField()

