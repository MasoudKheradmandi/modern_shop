from django import forms
from django.core.exceptions import ValidationError

from home.models import NewsLatter

class NewsLetterForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data.get('email',None)
        if email is None:
            raise ValidationError('email must be send')
        
        newsletter = NewsLatter.objects.filter(email=email).first()
        if newsletter is None:
            newsletter = NewsLatter.objects.create(email=email)

        return self.cleaned_data
