from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


# 商品详情页
def detail(request):
    return render(request, 'detail.html')
