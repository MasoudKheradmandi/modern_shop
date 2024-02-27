from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy

import jdatetime

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


class CartListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")

    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        order , created = Order.objects.get_or_create(profile=profile,in_proccesing=False)

        if created or not order.orderitem_set.exists():
            return render(request,'cart-empty.html')

        context = {
            'order' : order,  # TODO: we need better quary to avoid n+1 problem (select related?)
        }
        return render(request,'cart.html',context)


class DeleteCartItemView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")

    def get(self,request,order_item_id):
        order_item = OrderItem.objects.filter(id=order_item_id,order__profile__user=request.user)
        if order_item.exists():
            order_item.delete()
            msg = 'محصول با موفقیت از سبد خرید شما حذف شد'
            messages.success(request,msg)
        else:
            msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره امتحان کنید.'
            messages.error(request,msg)
        return redirect("cart:cart-list")


class ChangeOrderItemQuantityView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")

    def get(self,request):
        form = AddToCartForm(request.GET)
        if form.is_valid():
            product_variation = form.cleaned_data.get('product_variant')
            quantity = form.cleaned_data.get('quantity')
            OrderItem.objects.filter(product_variant=product_variation).update(quantity=quantity)
            msg = 'تعداد محصول با موفقیت تغییر کرد'
        else:
            msg = 'مشکلی در سیستم رخ داده است. لطفا بعدا دوباره امتحان کنید.'

        return JsonResponse({'msg':msg})


class ShippingView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")
    def get(self,request):
        jdatetime.set_locale(jdatetime.FA_LOCALE)
        today = jdatetime.date.today()

        start_delta_time = jdatetime.timedelta(days=4)
        finish_delta_time = jdatetime.timedelta(days=8)

        start_date = today + start_delta_time
        finish_date = today + finish_delta_time

        formatted_start_date = f"{start_date.year}-{start_date.jmonth()}-{start_date.day}"
        formatted_finish_date = f"{finish_date.year}-{finish_date.jmonth()}-{finish_date.day}"

        context = {
            'start_date' : formatted_start_date,
            'finish_date' : formatted_finish_date,
        }
        return render(request,'shipping-payment.html',context)


class ProfileCart(View):
    def get(self,request):
        user = Profile.objects.get(user = request.user)
        orders = Order.objects.filter(profile=user)
        context = {
            'orders':orders,
        }
        ##
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

