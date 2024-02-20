from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from cart.models import OrderItem
from product.models import TvSize


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_variant','quantity']

    def clean(self) -> dict[str, Any]:
        product_variation = self.cleaned_data.get('product_variant',None)
        if product_variation is None:
            raise ValidationError("some error caused.pleas try again later")

        product = product_variation.product
        if product.is_show == False:
            raise ValidationError("some error caused.pleas try again later")

        quantity = self.cleaned_data.get('quantity')
        if quantity < 1 :
            raise ValidationError("some error caused.pleas try again later")

        if quantity > product_variation.count :
            raise ValidationError("تعداد انتخابی شما بیشتر از موجودی انبار می باشد")

        return self.cleaned_data

