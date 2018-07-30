from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    # 用户模型类


    class Meta:
        db_table = 'usr_user'
        verbose_name_plural = '用户'


class AddressManager(models.Manager):
    # 地址模型管理器类
    def get_default_address(self, user):
        try:
            address = self.get(user=user, is_default=True)  # models.Manager
        except self.model.DoesNotExist:
            address = None
        return address

class Address(BaseModel):
    # 地址模型类
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义模型管理器对象
    objects = AddressManager()

    class Meta:
        db_table = 'usr_address'
        verbose_name_plural = '地址'

