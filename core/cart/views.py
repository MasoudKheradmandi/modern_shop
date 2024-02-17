from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib import messages

from cart.forms import AddToCartForm
# Create your views here.
import logging
logger = logging.getLogger(__name__)

class AddToCart(View):
    def get(self,request):
        form = AddToCartForm(request.GET)
        if form.is_valid():
            pass
        else:
            # error_msg = 'مشکلی پیش امده است لطفا دوباره تلاش کنید.'
            messages.error(request,form.errors)

        path = request.GET.get('next','/')
        return redirect(path)


