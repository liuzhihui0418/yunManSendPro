from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, Order, Category, CartItem
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, CartItemSerializer


# ============================
# 1. 注册接口
# ============================
@api_view(['POST'])
def register(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    if not phone or not password:
        return Response({'code': 400, 'msg': '手机号或密码不能为空'})
    if User.objects.filter(username=phone).exists():
        return Response({'code': 400, 'msg': '该手机号已注册'})
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
    user = authenticate(username=phone, password=password)
    if user is not None:
        return Response({
            'code': 200,
            'msg': '登录成功',
            'data': {'user_id': user.id, 'username': user.username}
        })
    else:
        return Response({'code': 400, 'msg': '账号或密码错误'})


# ============================
# 3. 业务视图 (分类、商品、订单、购物车)
# ============================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('sort')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    # 1. 查询购物车：允许用 ?user_id=xxx 过滤
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return CartItem.objects.filter(user_id=user_id).order_by('-created_at')
        return CartItem.objects.none()

    # 2. 加入购物车：自动处理数量叠加
    def create(self, request, *args, **kwargs):
        # 获取前端传来的 user 和 product
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        # 检查是否已存在
        existing_item = CartItem.objects.filter(user_id=user_id, product_id=product_id).first()

        if existing_item:
            # 存在则增加数量
            existing_item.quantity += quantity
            existing_item.save()
            return Response({'status': 'updated', 'id': existing_item.id}, status=200)
        else:
            # 不存在则创建新条目
            return super().create(request, *args, **kwargs)