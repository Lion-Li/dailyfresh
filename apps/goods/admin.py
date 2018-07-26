from django.contrib import admin
from apps.goods.models import GoodsSPU # 从models中导入goods_spu模型类

# 创建管理员账户: python manage.py createsuperuser
admin.site.register(GoodsSPU)  # 在后台管理注册模型
