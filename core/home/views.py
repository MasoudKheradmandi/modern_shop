from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages


from home.models import Navbar , SiteSettings , Footer , Slider
from home.forms import NewsLetterForm
from product.models import Product
from account.models import Profile


class HomeView(View):
    def get(self,request):
        sliders = Slider.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        context = {
            'sliders' : sliders,
            'site_setting' : site_setting,
        }
        return render(request,'index.html',context)


class HeaderView(View):
    def get(self,request):
        profile = Profile.objects.filter(user=request.user.id)
        navbars = Navbar.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        context = {
            'profile' : profile,
            'navbars' : navbars,
            'site_setting' : site_setting,
        }
        return render(request,'layout/header.html',context)


class FooterView(View):
    def get(self,request):
        footers = Footer.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        context = {
            'footers' : footers,
            'site_setting' : site_setting,
        }
        return render(request,'layout/footer.html',context)

    def post(self,request):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            messages.success(request,'ایمیل شما با موفقیت ثبت شد.')
        else:
            messages.error(request,'مشکلی پیش امده است لطفا دوباره تلاش کنید.')

        return redirect('home:index-page')


