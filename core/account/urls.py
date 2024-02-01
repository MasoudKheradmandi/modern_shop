
from django.urls import path
from account.views import LoginView , LoginVerificationView , WelcomePageView

app_name="account"


urlpatterns = [
    path('login/', LoginView.as_view(),name='login-page'),
    path('login-verification/', LoginVerificationView.as_view(),name='login-verification-page'),
    path('welcome/', WelcomePageView.as_view(),name='welcome-page'),


]



