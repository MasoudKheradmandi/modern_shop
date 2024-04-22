from django.urls import path
from . import views

app_name='product'

urlpatterns = [
    path('listview/',views.ProductListView.as_view(),name='listview'),
    path('<str:category>/<int:id>/',views.ProductDetailView.as_view(),name='detail'),
    path('wishlist/',views.WishListView.as_view(),name='wish_list'),
    path('search/',views.Search.as_view(),name='search'),
    path('log/',views.login_view,),
]
