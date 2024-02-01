from random import randint
from django.shortcuts import render , redirect
from django.views.generic import View

from account.forms import LoginForm
# Create your views here.

class LoginView(View):
    def get(self,request):
        context = {}
        return render(request,'login.html',context)

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            random_code = randint(1000,10000)
            # TODO:send sms
            print(phone_number,random_code)
            redirect('account:login-verfication')
        else:
            errors = form.errors
            # TODO: show error to  user
            return redirect('account:login-page')
