from django import forms
from django.core.exceptions import ValidationError

from account.models import User, Profile, validate_phone_number, validate_verification_code

class LoginForm(forms.Form):
    phone_number = forms.CharField(validators=[validate_phone_number])

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number',None)
        if phone_number is None:
            raise ValidationError('the phone_number must be set')
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            user = User.objects.create_user(phone_number=phone_number)

        self.cleaned_data.update({'user':user})
        return self.cleaned_data




class LoginVerificationForm(forms.Form):
    verify_code = forms.IntegerField(validators=[validate_verification_code])

class ProfileAddInfoForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('shop_point','user')
