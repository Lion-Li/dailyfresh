from django.urls import path
from apps.goods import views

app_name = 'goods'
urlpatterns = [
    path('detail/', views.detail, name='detail'),
    path('index/', views.index, name='index'),
    path('', views.index),
]
