from django.urls import path
from home.views import HomeView , HeaderView , FooterView
from django.views.decorators.cache import cache_page
app_name='home'

urlpatterns = [
    path('', cache_page(15 * 1)(HomeView.as_view()),name='index-page'),
    path('header/', HeaderView.as_view(),name='header-layout'),
    path('footer/', FooterView.as_view(),name='footer-layout'),

]
