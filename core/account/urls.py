
from django.urls import path
from account.views import (LoginView , LoginVerificationView , WelcomePageView , LogoutView,
                           ProfileView,ProfileAddInfoView)


app_name="account"


urlpatterns = [
    # account
    path('login/', LoginView.as_view(),name='login-page'),
    path('login-verification/', LoginVerificationView.as_view(),name='login-verification-page'),
    path('welcome/', WelcomePageView.as_view(),name='welcome-page'),
    path('logout/', LogoutView.as_view(),name='logout-page'),

    # profile
    path('profile/', ProfileView.as_view(),name='profile-page'),
    path('profile-add-info/', ProfileAddInfoView.as_view(),name='profile-add-info-page'),

]



