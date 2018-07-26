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


# 显示注册页面
def register(request):
    return render(request, 'register.html')


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


# 用户注册
class RegisterView(View):
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 注册处理

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
            usr = User.objects.create_user(username, password, email)
            usr.is_active = 0
            usr.save()


        return redirect(reverse('goods:index'))


    #   ```````````````````

