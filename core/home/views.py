from django.shortcuts import render
from django.views.generic import View
# Create your views here.

class HomeView(View):
    def get(self,request):
        context = {}
        return render(request,'index.html',context)

