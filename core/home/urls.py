from django.urls import path
from home.views import HomeView , HeaderView , FooterView

app_name='home'

urlpatterns = [
    path('', HomeView.as_view(),name='index-page'),
    path('header/', HeaderView.as_view(),name='header-layout'),
    path('footer/', FooterView.as_view(),name='footer-layout'),

]
