from django.urls import path, re_path
from apps.usr.views import RegisterView, ActiveView, LoginView, verify_code

app_name = 'usr'
urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),  # 注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 通过邮箱激活用户
    re_path(r'^login/?$', LoginView.as_view(), name='login'),  # 登录页面
    path('verify_code/', verify_code, name='verify_code'),  # 图片验证码生成
]
