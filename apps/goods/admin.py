from django.contrib import admin
from apps.goods.models import GoodsType

# 创建管理员账户: python manage.py createsuperuser
admin.site.register(GoodsType)  # 在后台管理注册模型
