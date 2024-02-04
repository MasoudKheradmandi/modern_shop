from random import randint

from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import login , logout
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from account.forms import LoginForm , LoginVerificationForm
from account.models import User , Profile
# Create your views here.

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        context = {}
        return render(request,'login.html',context)

    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            user_obj = form.cleaned_data.get('user')
            self._set_user_token(user_obj)
            response = redirect('account:login-verification-page')
            response.set_cookie('user_phone_number',phone_number,1000)
            return response
        else:
            errors = 'لطفا یک شماره معتبر وارد کنید'
            messages.error(request,errors)
            return redirect('account:login-page')

    def _set_user_token(self,user_obj):
        random_code = randint(1000,100000)
        user_obj.token = random_code
        user_obj.save()
        # TODO: send token with sms


class LoginVerificationView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        # context = {}
        #  TEMP
        phone_number = request.COOKIES.get('user_phone_number',None)
        context = {'token':User.objects.filter(phone_number=phone_number).first().token}
        return render(request,'login-verification.html',context)

    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
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

            login(request,user)
            return redirect('account:welcome-page')
        else:
            errors = form.errors
            messages.error(request,errors)
            return redirect('account:login-verification-page')


class WelcomePageView(View):
    def get(self,request):
        if request.user.is_anonymous:
            return redirect('home:index-page')
        context = {}
        return render(request,'welcome.html',context)


class LogoutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request,'شما با موفقیت از حساب کاربری خود خارج شدید')
        return redirect("account:login-page")

class ProfileView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")

    def get(self,request):
        profile = get_object_or_404(Profile,user=request.user)
        context = {
            'profile' : profile,
            'user' : request.user,
        }
        return render(request,'profile.html',context)

class ProfileAddInfoView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")

    def get(self,request):
        context = {}
        return render(request,'profile-additional-info.html',context)

    def post(self,request):
        pass
