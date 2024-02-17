from django.urls import path
from cart.views import AddToCart

app_name='cart'

urlpatterns = [
    path('add-to-cart/',AddToCart.as_view(),name='add-to-cart')
]
