from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# ============================
# 1. 注册接口
# ============================
@api_view(['POST'])
def register(request):
    phone = request.data.get('phone')
    password = request.data.get('password')

    if not phone or not password:
        return Response({'code': 400, 'msg': '手机号或密码不能为空'})

    # 检查手机号是否已存在
    if User.objects.filter(username=phone).exists():
        return Response({'code': 400, 'msg': '该手机号已注册'})

    # 创建用户 (这里把手机号当做用户名存)
    user = User.objects.create_user(username=phone, password=password)
    user.save()

    return Response({'code': 200, 'msg': '注册成功', 'data': {'id': user.id, 'name': phone}})

# ============================
# 2. 登录接口
# ============================
@api_view(['POST'])
def login_view(request):
    phone = request.data.get('phone')
    password = request.data.get('password')

    # Django 自带的验证方法
    user = authenticate(username=phone, password=password)

    if user is not None:
        # 登录成功，返回用户信息
        return Response({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'token': 'fake-token-' + str(user.id) # 暂时用个假token模拟
            }
        })
    else:
        return Response({'code': 400, 'msg': '账号或密码错误'})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

