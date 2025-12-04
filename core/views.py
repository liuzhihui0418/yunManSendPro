from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, Order, CartItem
from .serializers import ProductSerializer, OrderSerializer, CartItemSerializer
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


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    # 只返回当前登录用户的购物车
    def get_queryset(self):
        # 如果没登录(比如后台管理)，返回空或者所有
        if self.request.user.is_anonymous:
            return CartItem.objects.none()
        return CartItem.objects.filter(user=self.request.user).order_by('-created_at')

    # 创建时自动填入当前用户
    def perform_create(self, serializer):
        # 检查该用户是否已经加购过该商品，如果有，只加数量
        product = serializer.validated_data['product']
        user = self.request.user
        existing_item = CartItem.objects.filter(user=user, product=product).first()

        if existing_item:
            existing_item.quantity += serializer.validated_data['quantity']
            existing_item.save()
        else:
            serializer.save(user=user)