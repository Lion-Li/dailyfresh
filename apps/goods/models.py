from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField  # pip install django-tinymce


class GoodsType(BaseModel):
    # 商品类型表
    name = models.CharField(max_length=20, verbose_name='商品种类名称')
    logo = models.CharField(max_length=20, verbose_name='商品标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    class Meta:
        db_table = 'goods_type'
        verbose_name = '商品类型'
        verbose_name_plural = '商品类型'

    def __str__(self):
        return self.name
class GoodsSKU(BaseModel):
    # 商品SKU表
    status_choice = (
        (0, '下线'),
        (1, '上线'),
    )

    # 设置外键
    type = models.ForeignKey('GoodsType', verbose_name='商品种类', on_delete=models.CASCADE)
    goods = models.ForeignKey('GoodsSPU', verbose_name='商品SPU', on_delete=models.CASCADE)

    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods_spu', verbose_name='商品图片')
    stock = models.IntegerField(default=9999, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status_choice = models.SmallIntegerField(default=0, choices=status_choice, verbose_name='商品状态')

    class Meta:
        db_table = 'goods_sku'
        verbose_name_plural = '商品SKU'

    # def __str__(self):
    #     return self.name


class GoodsSPU(BaseModel):
    # 商品spu表
    name = models.CharField(max_length=100, verbose_name='商品名称')
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'goods_spu'
        verbose_name_plural = '商品SPU表'

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    # 商品图片模型类
    sku = models.ForeignKey('GoodsSPU', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    class Meta:
        db_table = 'goods_image'
        verbose_name_plural = '商品图片'


class GoodsIndexBanner(BaseModel):
    # 首页轮播商品展示模型类
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'goods_index_banner'
        verbose_name_plural = '首页轮播商品'


class GoodsIndexType(BaseModel):
    # 首页分类商品展示模型类
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型', on_delete=models.CASCADE)
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU', on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'goods_index_type'
        verbose_name_plural = "主页分类展示商品"


class GoodsIndexPromotion(BaseModel):
    # 首页促销活动模型类
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'goods_index_promotion'
        verbose_name_plural = "主页促销活动"



