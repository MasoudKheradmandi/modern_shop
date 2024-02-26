from django.urls import path
from cart import views

app_name='cart'

urlpatterns = [
    path('add-to-cart/',views.AddToCart.as_view(),name='add-to-cart'),
    path('profile-order/',views.ProfileCart.as_view(),name='profile-order'),
    path('profile-order/<str:pk>',views.Factor.as_view(),name='profile-order'),#TODO:fix this
    path('cart-list/',views.CartListView.as_view(),name='cart-list'),
    path('delete-cart-item/<int:order_item_id>/',views.DeleteCartItemView.as_view(),name='delete-cart-item'),
    path('change-cart-quantity/',views.ChangeOrderItemQuantityView.as_view(),name='change-cart-quantity'),
    path('shipping/',views.ShippingView.as_view(),name='shipping-page'),

]
