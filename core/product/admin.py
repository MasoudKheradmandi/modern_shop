from django.contrib import admin
from .models import Product,Category,Comment,TvSize,DiscountCode,WishList
# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(TvSize)
admin.site.register(DiscountCode)

admin.site.register(WishList)