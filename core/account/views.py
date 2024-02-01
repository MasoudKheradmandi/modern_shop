from random import randint
from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages
from account.forms import LoginForm , LoginVerificationForm
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
            user_obj = form.cleaned_data.get('user')
            self._set_user_token(user_obj)
            response = redirect('account:login-verification-page')
            response.set_cookie('user_phone_number',phone_number,1000)
            return response
        else:
            errors = form.errors
            messages.error(request,errors)
            return redirect('account:login-page')

    def _set_user_token(self,user_obj):
        random_code = randint(1000,100000)
        user_obj.token = random_code
        user_obj.save()
        # TODO: send token with sms


class LoginVerificationView(View):
    def get(self,request):
        context = {}
        return render(request,'login-verification.html',context)

    def post(self,request):
        form = LoginVerificationForm(request.POST)
        if form.is_valid():
            verify_code = form.cleaned_data.get('verify_code')
            phone_number = request.COOKIES.get('user_phone_number',None)
            user = User.objects.filter(phone_number=phone_number).first()

            if user is None:
                error_msg = 'مشکلی داخل سیستم رخ داده است,لطفا دویاره امتحان کنید.'
                messages.error(request,error_msg)
                return redirect('account:login-page')


            if int(user.token) == verify_code:
                user.is_verified = True
                user.save()
            else:
                error_msg = 'کد وارد شده اشتباه می باشد'
                messages.error(request,error_msg)
                return redirect('account:login-verification-page')

            self._verify_user(request,user,verify_code)
            return redirect('account:welcome-page')
        else:
            errors = form.errors
            messages.error(request,errors)
            return redirect('account:login-verification-page')


class WelcomePageView(View):
    def get(self,request):
        context = {}
        return render(request,'welcome.html',context)

