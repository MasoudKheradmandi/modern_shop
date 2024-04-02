
from django.urls import path , include
from account.views import (LoginView , LoginVerificationView, ProfileWishListView
                           , WelcomePageView, LogoutView, ProfileView, ProfileAddInfoView,ProfileSideBarView
                           ,ProfileCart,Factor)


app_name="account"


urlpatterns = [
    # account
    path('login/', LoginView.as_view(),name='login-page'),
    path('login-verification/', LoginVerificationView.as_view(),name='login-verification-page'),
    path('welcome/', WelcomePageView.as_view(),name='welcome-page'),
    path('logout/', LogoutView.as_view(),name='logout-page'),

    # profile
    path('profile-sidebar/', ProfileSideBarView.as_view(),name='profile-sidebar'),
    path('profile/', ProfileView.as_view(),name='profile-page'),
    path('profile-add-info/', ProfileAddInfoView.as_view(),name='profile-add-info-page'),
    path('profile-wish-list/', ProfileWishListView.as_view(),name='profile-wish-list-page'),
    # path('profile-order-list/', ProfileOrderListView.as_view(),name='profile-order-list-page'),
    path('profile-order/',ProfileCart.as_view(),name='profile-order-list-page'),
    path('profile-order-factor/<str:pk>',Factor.as_view(),name='factor-page'),



]



