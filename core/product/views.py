from django.shortcuts import render
from django.views import View
from .models import Product,TvSize
import logging
# Create your views here.


logger = logging.getLogger(__name__)
class ProductListView(View):

    def get(self,request):
        product_obj = Product.objects.filter(is_show=True)
        context = {'product_obj':product_obj}
        return render(request,'listview.html',context)
    
    def post(self,request):
        pass

class ProductDetailView(View):
    def get(self,request,category,id):
        obj = Product.objects.get(id=id,is_show=True)
        context = {
            'obj':obj
        }
        return render(request,'detail.html',context)

    def post(self,request):
        pass
