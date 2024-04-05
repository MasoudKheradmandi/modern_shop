from django.contrib import admin
from .models import Product,Category,Comment,TvSize,WishList
# Register your models here.

class TvSizeInline(admin.TabularInline):
    model = TvSize
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = [TvSizeInline,]

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(TvSize)
admin.site.register(WishList)
