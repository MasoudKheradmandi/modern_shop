from django import forms

from account.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number',)

