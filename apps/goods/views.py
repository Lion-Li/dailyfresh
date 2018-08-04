from django.shortcuts import render
from apps.goods.models import *


def index(request):
    """
        网站首页的视图函数
        从数据库获取各类信息来渲染模板
    """
    goods_type = GoodsType.objects.all()
    goods_banner = GoodsIndexBanner.objects.all().order_by('index')
    goods_promotion = GoodsIndexPromotion.objects.all().order_by('index')
    # # goods_index_type = GoodsIndexType.objects.all()
    for type in goods_type:  # GoodsType
        type.title_banner = GoodsIndexType.objects.filter(type=type, display_type=0).order_by('index')
        type.image_banner = GoodsIndexType.objects.filter(type=type, display_type=1).order_by('index')
    cart_count = 0  # 购物车商品数

    context = {
        'goods_type': goods_type,
        'goods_banner': goods_banner,
        'goods_promotion': goods_promotion,
        'cart_count': cart_count
    }
    return render(request, 'index.html', context)


# 商品详情页
def detail(request):
    return render(request, 'detail.html')
