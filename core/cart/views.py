from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages
from django.db.models import Sum
from cart.forms import AddToCartForm
from cart.models import Order , OrderItem
from account.models import Profile
# Create your views here.


import logging
logger = logging.getLogger(__name__)

class AddToCart(View):
    def get(self,request):
        form = AddToCartForm(request.GET)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            product_variation = form.cleaned_data.get('product_variant')
            product = form.cleaned_data.get('product')
            quantity = form.cleaned_data.get('quantity')
            final_price = product.price + product_variation.price_difference
            discount = 0 if product_variation.discount is None else product_variation.discount.discountـpercent

            order , _ = Order.objects.get_or_create(profile=profile,in_proccesing=False)

            order_item = OrderItem.objects.filter(order_id=order.id,product_variant=product_variation)
            if order_item.exists():
                msg = 'این محصول در سبد خرید شما وجود دارد'
                messages.info(request,msg)
            else:
                OrderItem.objects.create(order=order,product_variant=product_variation,final_price=final_price,
                                         calculated_discount=discount,quantity=quantity)
                msg = 'این محصول با موفقیت به سبد محصول شما اضافه شد'
                messages.success(request,msg)
        else:
            # error_msg = 'مشکلی پیش امده است لطفا دوباره تلاش کنید.'
            messages.error(request,form.errors.get('__all__'))

        path = request.GET.get('next','/')
        return redirect(path)


class ProfileCart(View):
    def get(self,request):
        user = Profile.objects.get(user = request.user)
        orders = Order.objects.filter(profile=user)
        context = {
            'orders':orders,
        }
        return render(request,'profile-order.html',context)
    

class Factor(View):
    def get(self,request,pk):
        order = Order.objects.get(shopping_id=pk)
        order_detail = OrderItem.objects.filter(order=order)
        total_price = order_detail.aggregate(
            total_price=Sum('final_price')
        ) # TODO : fox this   {'total_price': Decimal('950000.00')}


        logger.warning(total_price['total_price'])
        context = {
            'order_det':order,
            'products':order_detail,
            'total_price':total_price['total_price']
        }
        return render(request,'factor.html',context)

