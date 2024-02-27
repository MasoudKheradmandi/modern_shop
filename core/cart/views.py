import requests
import json

from django.shortcuts import render , redirect ,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum , F
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy , reverse
from django.conf import settings
from django.utils import timezone

from cart.forms import AddToCartForm
from cart.models import Order , OrderItem
from account.models import Profile
from product.models import TvSize
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
        order , created = Order.objects.prefetch_related('orderitem_set').get_or_create(profile=profile,in_proccesing=False)

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
        profile = Profile.objects.get(user=request.user)
        order , created = Order.objects.prefetch_related('orderitem_set').get_or_create(profile=profile,in_proccesing=False)
        if  not order.orderitem_set.exists():
            return render(request,'cart-empty.html')

        context = {
            'order' : order,
        }
        return render(request,'shipping-payment.html',context)


class PaymentView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.filter(profile=profile,in_proccesing=False).last()

        if  not order.orderitem_set.exists():
            return render(request,'cart-empty.html')

        CallbackURL = request.build_absolute_uri(reverse('cart:verify'))

        data = {
        "MerchantID": settings.MERCHANTID,
        "Amount": order.calculate_paid_amount_needed(),
        "Description": "این تراکنش صرفا جهت تست می باشد",
        "Phone": 'YOUR_PHONE_NUMBER',
        "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data,headers=headers, timeout=100)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return redirect(settings.ZP_API_STARTPAY + str(response['Authority']))
                else:
                    messages.error(request,str(response['Status']))
                    return redirect('cart:shipping-page')
            return JsonResponse(response.json(),safe=False)

        except requests.exceptions.Timeout:
            # return {'status': False, 'code': 'timeout'}
            messages.error(request,'timeout')
            return redirect('cart:shipping-page')
        except requests.exceptions.ConnectionError:
            # return {'status': False, 'code': 'connection error'}
            messages.error(request,'connection error')
            return redirect('cart:shipping-page')


class AfterPaymentView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")
    @transaction.atomic
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.prefetch_related('orderitem_set').filter(profile=profile,in_proccesing=False).last()

        if  not order.orderitem_set.exists():
            return render(request,'cart-empty.html')

        amount = order.calculate_paid_amount_needed()
        data = {
        "MerchantID": settings.MERCHANTID,
        "Amount": amount,
        "Authority": request.GET.get('Authority'),
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(settings.ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            ref_id = response['RefID']
            if response['Status'] == 100:
                self.save_order_and_orderitem_data(request.user.phone_number,profile,amount)
                return redirect('cart:success-payment-page',order_id=order.id)
            else:
                return redirect('cart:failure-payment-page',order_id=order.id)
        return JsonResponse(response.json(),safe=False)

    @transaction.atomic
    def save_order_and_orderitem_data(self,phone_number,profile,amount) -> None:
        now = timezone.now()
        order = Order.objects.filter(profile=profile,in_proccesing=False)
        order.update(full_name=profile.full_name,address=profile.address,phone_number=phone_number,
                        paid_amount=amount,in_proccesing=True,payment_date=now) # update order

        order = Order.objects.prefetch_related('orderitem_set').get(profile=profile,in_proccesing=True,payment_date=now)
        for order_item in order.orderitem_set.all(): # update order items
            order_item.final_price= order_item.product_variant.price_difference + order_item.product_variant.product.price
            order_item.selected_size = order_item.product_variant.size
            order_item.save()

            TvSize.objects.filter(id=order_item.product_variant.id).update(count=F('count') - order_item.quantity)


class SucessPaymentView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")
    def get(self,request,order_id):
        order = get_object_or_404(Order,id=order_id)
        context = {
            'order' : order
        }
        return render(request,'shipping-complate-buy.html',context)


class FailurePaymentView(LoginRequiredMixin,View):
    login_url = reverse_lazy("account:login-page")
    def get(self,request,order_id):
        order = get_object_or_404(Order,id=order_id)
        context = {
            'order' : order
        }
        return render(request,'shipping-no-complate-buy.html',context)


