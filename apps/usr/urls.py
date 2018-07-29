from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from apps.usr.views import RegisterView, ActiveView, LoginView, verify_code, user_center_info
from apps.usr import views
app_name = 'usr'
urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),  # 注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 通过邮箱激活用户
    re_path(r'^login/?$', LoginView.as_view(), name='login'),  # 登录页面
    path('verify_code/', views.verify_code, name='verify_code'),  # 图片验证码生成
    path('user_center_info', login_required(views.user_center_info), name='user_center_info'),  # 用户中心-个人信息页
    path('user_center_order', login_required(views.user_center_order), name='user_center_order'),  # 用户中心-订单页
    path('user_center_address', login_required(views.user_center_address), name='user_center_address'),  # 用户中心-地址页
]
