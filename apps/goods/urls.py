from django.urls import path
from apps.goods import views

app_name = 'goods'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index),
]
