from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام دسته بندی')
    image = models.ImageField(verbose_name='عکس دسته بندی')

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    count = models.PositiveIntegerField() # تعداد کد تخفیف برای محصول ->۵ نفر میتوانند استفاده کنند
    code_name = models.CharField(max_length=30)
    discountـpercent= models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)]) # درصد تخفیف

    def __str__(self):
        return self.code_name + " " + str(self.count)


class TvSize(models.Model):
    product = models.ForeignKey("Product",on_delete=models.PROTECT)
    size = models.CharField(max_length=4,verbose_name='سایز')
    price_difference = models.IntegerField(verbose_name='اختلاف قیمت',default=0)
    count = models.PositiveIntegerField() # تعداد تلویزیون با سایز مشخص یا همون موجودی انبار
    discount = models.OneToOneField(DiscountCode,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.product.name + " " + self.size




class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=450,verbose_name='نام محصول')
    image = models.ImageField(verbose_name="عکس محصول")
    image_1 = models.ImageField(verbose_name="عکس محصول",null=True)
    image_2 = models.ImageField(verbose_name="عکس محصول",null=True)
    image_3 = models.ImageField(verbose_name="عکس محصول",null=True)


    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    sales_number = models.IntegerField(default=0) #تعداد فروش
    price = models.PositiveIntegerField()

    specification = models.TextField()
    description = models.TextField()

    quality = models.IntegerField(null=True)
    pannel_type = models.CharField(max_length=250,null=True)
    port = models.CharField(max_length=450,null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    is_special = models.BooleanField(default=False)
    is_show = models.BooleanField(default=True)



    def __str__(self):
        return self.name



class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    author = models.ForeignKey("account.Profile",on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False,verbose_name='نمایش داده شود؟')

    def _answer(self):
        if self.answer:
            return 'جواب داده شد'
        else:
            return 'جواب داده نشد'

    def __str__(self):
        return str(self.is_show)+" "+self.product.name + " "+ str(self._answer())


class WishList(models.Model):
    profile = models.OneToOneField("account.Profile",on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.profile.full_name
