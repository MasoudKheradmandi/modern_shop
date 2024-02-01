from random import randint
from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages
from account.forms import LoginForm
from account.models import User
# Create your views here.

class LoginView(View):
    def get(self,request):
        # if request.user.is_authenticated:
        #     return redirect('/')
        context = {}
        return render(request,'login.html',context)

    def post(self,request):
        # if request.user.is_authenticated:
        #     return redirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            user_obj = User.objects.get(phone_number=phone_number)
            self._set_user_token(user_obj)
            redirect('account:login-verification-page')
        else:
            errors = form.errors
            messages.error(request,errors)
            return redirect('account:login-page')

    def _set_user_token(self,user_obj):
        random_code = randint(1000,10000)
        user_obj.token = random_code
        user_obj.save()
        # TODO: send token with sms

class LoginVerificationView(View):
    def get(self,request):
        context = {}
        return render(request,'login-verification.html',context)

    def post(self,request):
        pass
