from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Product, Order, Category, CartItem, Address
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, CartItemSerializer, AddressSerializer


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


# 找到 OrderViewSet，整个替换成下面这样：
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_queryset(self):
        # 1. 获取基础查询集
        queryset = Order.objects.all().order_by('-created_at')

        # 2. 过滤：只看当前用户的订单
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(customer_name=username)

        # 3. 过滤：按订单状态筛选
        status = self.request.query_params.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)

        return queryset

    # 重写创建订单逻辑
    def perform_create(self, serializer):
        # 1. 保存订单
        order = serializer.save()

        # 2. 获取前端传来的“暗号” (is_from_cart)
        # 注意：request.data 获取的是非模型字段
        is_from_cart = self.request.data.get('is_from_cart', False)

        # 3. 如果是购物车订单，并且有用户名，就清空该用户的购物车
        if is_from_cart is True or str(is_from_cart) == 'true':
            if order.customer_name:
                print(f"检测到购物车结算，正在清空 {order.customer_name} 的购物车...")
                # 通过用户名找到对应的 User，再删 CartItem
                CartItem.objects.filter(user__username=order.customer_name).delete()



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

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer

    # 只查当前登录用户的地址
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Address.objects.filter(user_id=user_id).order_by('-is_default', '-id')
        return Address.objects.none()

    # 创建/修改时，如果设为默认，把其他的默认取消掉
    def perform_create(self, serializer):
        if serializer.validated_data.get('is_default'):
            user = serializer.validated_data['user']
            Address.objects.filter(user=user).update(is_default=False)
        serializer.save()

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default'):
            user = serializer.instance.user
            Address.objects.filter(user=user).update(is_default=False)
        serializer.save()