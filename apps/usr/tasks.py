from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


# 发送注册激活邮件
@shared_task
def send_register_email(email, username, token):
    # 组织邮件内容
    subject = '注册激活'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h2>尊敬的%s,天天生鲜欢迎您的到来!</h2><br>' \
                   '<h4>请点击下面链接激活您的账户,链接将在一小时后失效.</h4><br>' \
                   '<a href="http://127.0.0.1:8000/usr/active/%s">http://127.0.0.1:8000/usr/active/%s</a>'\
                   % (username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)