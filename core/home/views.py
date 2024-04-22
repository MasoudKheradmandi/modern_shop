from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models.aggregates import Count


from home.models import Navbar , SiteSettings , Footer , Slider
from home.forms import NewsLetterForm
from product.models import Product , WishList
from account.models import Profile
from cart.models import Order , OrderItem


class HomeView(View):
    def get(self,request):
        sliders = Slider.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        all_products = Product.objects.filter(is_show=True).prefetch_related('tvsize_set').order_by('-updated_date')[:8]
        most_sell_products = Product.objects.filter(is_show=True).prefetch_related('tvsize_set').order_by('-sales_number')[:8]
        popular_products = Product.objects.filter(is_show=True).annotate(cat_count=Count('category__product')).prefetch_related('tvsize_set').order_by('-cat_count')[:8]

        context = {
            'sliders' : sliders,
            'site_setting' : site_setting,
            'all_products' : all_products,
            'most_sell_products' : most_sell_products,
            'popular_products' : popular_products,
        }
        return render(request,'index.html',context)


class HeaderView(View):
    def get(self,request):
        profile = Profile.objects.filter(user=request.user.id).first()
        navbars = Navbar.objects.all()
        site_setting = SiteSettings.objects.filter(is_active=True).last()
        wishlist = ''
        cart_items = ''
        if profile:
            wishlist = WishList.objects.filter(profile=profile).first()
            order = Order.objects.filter(profile=profile,in_proccesing=False).last()
            cart_items = OrderItem.objects.filter(order=order)
        # if:
        #     'sa'
        context = {
            'profile' : profile,
            'navbars' : navbars,
            'site_setting' : site_setting,
            'wishlist' : wishlist,
            'cart_items' : cart_items,
        }
        return render(request,'layout/header.html',context)


class FooterView(View):
    def get(self,request):
        footers = Footer.objects.all().prefetch_related('subfooter_set')
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


