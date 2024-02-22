from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse

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
            quantity = form.cleaned_data.get('quantity')

            order , _ = Order.objects.get_or_create(profile=profile,in_proccesing=False)

            order_item = OrderItem.objects.filter(order_id=order.id,product_variant=product_variation)
            if order_item.exists():
                msg = 'این محصول در سبد خرید شما وجود دارد'
                messages.info(request,msg)
            else:
                OrderItem.objects.create(order=order,product_variant=product_variation,
                                         quantity=quantity)
                msg = 'این محصول با موفقیت به سبد محصول شما اضافه شد'
                messages.success(request,msg)
        else:
            # error_msg = 'مشکلی پیش امده است لطفا دوباره تلاش کنید.'
            messages.error(request,form.errors.get('__all__'))

        path = request.GET.get('next','/')
        return redirect(path)


class CartListView(View):
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        order , created = Order.objects.get_or_create(profile=profile,in_proccesing=False)

        if created or not order.orderitem_set.exists():
            return render(request,'cart-empty.html')

        context = {
            'order' : order,  # TODO: we need better quary to avoid n+1 problem (select related?)
        }
        return render(request,'cart.html',context)


class DeleteCartItemView(View):
    def get(self,request,order_item_id):
        order_item = OrderItem.objects.filter(id=order_item_id)
        if order_item.exists():
            order_item.delete()
            msg = 'محصول با موفقیت از سبد خرید شما حذف شد'
            messages.success(request,msg)
        else:
            msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره انمتحان کنید.'
            messages.error(request,msg)
        return redirect("cart:cart-list")


class ChangeOrderItemQuantityView(View):
    def get(self,request):
        order_item_id = request.GET.get('order_item_id')
        quantity = request.GET.get('quantity_value')

        order_item = OrderItem.objects.filter(id=order_item_id)
        if order_item.exists() and int(quantity) >= 1:
            order_item.update(quantity=quantity)
            msg = 'تعداد محصول با موفقیت تغییر کرد'
        else:
            msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره انمتحان کنید.'
        return JsonResponse({'msg':msg})


class ProfileCart(View):
    def get(self,request):
        user = Profile.objects.get(user = request.user)
        orders = Order.objects.filter(profile=user)
        context = {
            'orders':orders,
        }
        #
        return render(request,'profile-order.html',context)


class Factor(View):
    def get(self,request,pk):
        order = Order.objects.get(shopping_id=pk)
        order_detail = OrderItem.objects.filter(order=order)
        total_price = order_detail.aggregate(
            total_price=Sum('final_price')
        )


        logger.warning(total_price['total_price'])
        context = {
            'order_det':order,
            'products':order_detail,
            'total_price':total_price['total_price']
        }
        return render(request,'factor.html',context)

