from django.urls import path
from cart import views

app_name='cart'

urlpatterns = [
    path('add-to-cart/',views.AddToCart.as_view(),name='add-to-cart'),
    path('cart-list/',views.CartListView.as_view(),name='cart-list'),
    path('delete-cart-item/<int:order_item_id>/',views.DeleteCartItemView.as_view(),name='delete-cart-item'),
    path('change-cart-quantity/',views.ChangeOrderItemQuantityView.as_view(),name='change-cart-quantity'),
    path('shipping/',views.ShippingView.as_view(),name='shipping-page'),

    path('request/', views.PaymentView.as_view(), name='request'),
    path('verify/', views.AfterPaymentView.as_view() , name='verify'),
    path('success-payment/<int:order_id>/', views.SuccessPaymentView.as_view() , name='success-payment-page'),
    path('failure-payment/<int:order_id>/', views.FailurePaymentView.as_view() , name='failure-payment-page'),


]
