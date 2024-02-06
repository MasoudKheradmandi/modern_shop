import logging
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from .models import Product,TvSize,Comment,WishList
from account.models import Profile,User
from django.contrib.auth import login
# Create your views here.


logger = logging.getLogger(__name__)
class ProductListView(View):

    def get(self,request):
        product_obj = Product.objects.filter(is_show=True)
        for x in product_obj:
            logger.warning(x.id)
        context = {'product_obj':product_obj}
        return render(request,'listview.html',context)
    
    def post(self,request):
        pass

class ProductDetailView(View):
    def get(self,request,category,id):
        obj = Product.objects.get(id=id,is_show=True)
        obj_size = TvSize.objects.filter(product=obj)
        comment = Comment.objects.filter(product=obj,is_show=True).order_by('-created_date')
        context = {
            'obj':obj,'obj_size':obj_size,'comments':comment
        }
        return render(request,'detail.html',context)

    def post(self,request,category,id):
        if request.user.is_authenticated:
            obj = Product.objects.get(id=id,is_show=True)
            profile =Profile.objects.get(user=request.user)
            if Comment.objects.filter(author=profile).count() > 2:
                messages.error(request,'شما نمیتوانید بیشتر از سه کامنت برای یک محصول ثبت کنید')
                return redirect('product:detail',category,id)
            else:
                text = request.POST.get('text')
                Comment.objects.create(product=obj,author=profile,text=text)
                messages.success(request,'پیام شما با موفقیت دریافت شد')
                return redirect('product:detail',category,id)
        else:
            messages.error(request,'لطفا ابتدا وارد حساب کاربری خود شوید')
            return redirect('product:detail',category,id)
        


class WishListView(View):
    def get(self,request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            obj = WishList.objects.filter(profile=profile).first()

            if obj:
                obj = obj.product.all()
                context = {'products':obj,'obj_count':obj.count()}
                return render(request,'wishlist.html',context)
            else:
                msg = 'سبد علاقمندی های شما خالی است'
                return render(request,'wishlist.html',{'obj_count':0,'msg':msg})

        else:
            messages.error(request,'ابتدا وارد حساب کاربری خود شوید')
            return redirect('/')




def login_view(request):
    username = '09033152968'
    user = User.objects.get(phone_number=username)
    logger.warning(user)
    if user is not None:
        login(request,user)
        return HttpResponse('s')
    return HttpResponse('d')