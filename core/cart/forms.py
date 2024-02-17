from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from cart.models import OrderItem
from product.models import TvSize


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['order','final_price','calculated_discount']

    def clean(self) -> dict[str, Any]:
        product_variant_id = self.cleaned_data.get('product_variant',0)

        product_variation = TvSize.objects.filter(id=product_variant_id).first()
        if product_variation is None:
            raise ValidationError("some error caused.pleas try again later.1")

        product = product_variation.product
        if product.is_show == False:
            raise ValidationError("some error caused.pleas try again later.2")


        quantity = self.cleaned_data.get('quantity',0)
        if quantity > product_variation.count :
            raise ValidationError("تعداد انتخابی شما بیشتر از موجودی انبار می باشد.3")

