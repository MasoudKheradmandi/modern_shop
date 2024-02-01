from django import forms

from account.models import validate_phone_number , validate_verification_code , User

class LoginForm(forms.Form):
    phone_number = forms.CharField(validators=[validate_phone_number])

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            user = User.objects.create_user(phone_number=phone_number)

        self.cleaned_data.update({'user':user})
        return self.cleaned_data




class LoginVerificationForm(forms.Form):
    verify_code = forms.IntegerField(validators=[validate_verification_code])
