from django.urls import path
from apps.cart import views

app_name = 'cart'
urlpatterns = [
    path('cart', views.cart, name='cart'),
]
