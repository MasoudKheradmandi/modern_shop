from django.shortcuts import render
from django.views.generic import View

from home.models import Navbar , SiteSettings , Footer
from product.models import Product

class HomeView(View):
    def get(self,request):

        context = {}
        return render(request,'index.html',context)

class HeaderView(View):
    def get(self,request):
        navbars = Navbar.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        context = {
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


