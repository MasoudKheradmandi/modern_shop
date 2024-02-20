from django.urls import path
from cart import views

app_name='cart'

urlpatterns = [
    path('add-to-cart/',views.AddToCart.as_view(),name='add-to-cart'),
    path('profile-order/',views.ProfileCart.as_view(),name='profile-order'),
    path('profile-order/<str:pk>',views.Factor.as_view(),name='profile-order'),#TODO:fix this
    path('cart-list/',views.CartListView.as_view(),name='cart-list'),

]
