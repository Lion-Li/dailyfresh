from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

# 验证码生成
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO

# 用户注册
from django.views.generic import View
from apps.usr.models import User
import re

# 邮箱
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from apps.usr.tasks import send_register_email

# 用户认证
from django.contrib.auth import authenticate, login


# 验证码生成
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# info加密解密模块
class Verify(object):
    def __init__(self):
        # 用settings中已有的秘钥来加密信息, 生成token.
        self.serializer = Serializer(settings.SECRET_KEY, 3600)

    # 加密用户信息
    def encypt_info(self, info):
        token = self.serializer.dumps(info)  # token为byte类型数据
        token = token.decode('utf8')  # 编码为utf8
        return token

    # 解密用户信息,创建用户的引用.
    def deciphering_info(self, token):
        # 解码加密信息
        info = self.serializer.loads(token)
        # 取出用户的id信息
        usr_id = info['confirm']
        # 创建对应用户的实例
        user = User.objects.get(id=usr_id)
        return user


# 用户登录
class LoginView(View):
    # 路由地址: /user/login
    # 通过继承Django内置的View(类视图),达到根据不同的请求方式调用不同的函数.

    def get(self, request):
        # 当浏览器get请求时,返回登录页面.
        # 如果cookie中有用户名,则使用模板时,用户名显示为记录的用户名,且'记住用户名'的复选框被选中.

        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # 当浏览器POST请求时,进行用户登录验证
        # authenticate()为Django内置的用户认证模块,如果账户和密码正确,返回值不为空.
        # redirect是HttpResponse的子类,有set_cookie的方法.
        # 通过GET请求获取登录后要跳转的页面,否则默认跳转到首页.

        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # print(username, password)

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '请输入用户名和密码'})

        user = authenticate(username=username, password=password)

        if user is not None:
            # 如果账户已激活
            if user.is_active == 1:
                # 记录用户的登录状态
                login(request, user)
                next_url = request.GET.get('next', 'goods:index')
                remember = request.POST.get('remember')
                response = redirect(next_url)

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# 激活用户
class ActiveView(View):
    def get(self, request, token):
        try:
            # 激活实例
            verify = Verify()
            user = verify.deciphering_info(token)
            # 激活用户
            user.is_active = 1
            # 提交到数据库
            user.save()
            # 返回到登录页面
            return redirect(reverse('usr:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期,请重新激活.')


# 用户注册
class RegisterView(View):
    # 显示注册页面
    def get(self, request):
        return render(request, 'register.html')

    # 注册处理
    def post(self, request):
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        yzm = request.POST.get('yzm')
        verifycode = request.session['verifycode']
        allow = request.POST.get('allow')

        # 验证数据
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '请填写完整信息'})

        if not re.match(r'^[a-zA-Z0-9][\w._-]*@[a-zA-Z0-9_-]+(.[a-zA-Z0-9]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '不同意协议无法为您服务'})

        # 校验验证码
        if yzm.upper() != verifycode:
            return render(request, 'register.html', {'errmsg': '验证码错误'})
        else:
            # 验证码通过后再将用户信息保存到数据库
            usr = User.objects.create_user(username, email, password)
            usr.is_active = 0
            usr.save()
            # 发送激活链接
            info = {'confirm': usr.id}
            verify_email = Verify()
            token = verify_email.encypt_info(info)
            # 发送邮件
            send_register_email.delay(email, username, token)
        return redirect(reverse('goods:index'))


# 用户中心-个人信息页
def user_center_info(request):
    return render(request, 'user_center_info.html', {'page': 'info'})


# 用户中心-订单页
def user_center_order(request):
    return render(request, 'user_center_order.html', {'page': 'order'})


# 用户中心-地址页
def user_center_address(request):
    return render(request, 'user_center_address.html', {'page': 'address'})



