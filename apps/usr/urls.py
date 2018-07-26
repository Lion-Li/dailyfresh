from django.urls import path, re_path
from apps.usr.views import RegisterView, verify_code

app_name = 'usr'
urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),  # 注册
    path('verify_code/', verify_code, name='verify_code'),  # 图片验证码生成
]
