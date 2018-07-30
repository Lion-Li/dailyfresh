from django.urls import path, re_path
from apps.usr.views import RegisterView, ActiveView, LoginView, LogoutView, UserCenterAddress
from apps.usr import views
app_name = 'usr'
urlpatterns = [
    re_path(r'^register/?$', RegisterView.as_view(), name='register'),  # 注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 通过邮箱激活用户
    re_path(r'^login/?$', LoginView.as_view(), name='login'),  # 调用登录视图
    re_path(r'^logout/?$', LogoutView.as_view(), name='logout'),  # 调用注销视图
    path('verify_code/', views.verify_code, name='verify_code'),  # 图片验证码生成
    path('user_center_info', views.user_center_info, name='user_center_info'),  # 用户中心-个人信息页
    path('user_center_order', views.user_center_order, name='user_center_order'),  # 用户中心-订单页
    path('user_center_address', UserCenterAddress.as_view(), name='user_center_address'),  # 用户中心-地址页
]
