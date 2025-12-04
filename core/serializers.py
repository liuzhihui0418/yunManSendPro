from rest_framework import serializers
from .models import Product, Order, Category, CartItem

# ============================
# 1. 分类序列化器 (之前报错缺这个)
# ============================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# ============================
# 2. 商品序列化器
# ============================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# ============================
# 3. 订单序列化器
# ============================
class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

# ============================
# 4. 购物车序列化器 (之前报错缺这个)
# ============================
class CartItemSerializer(serializers.ModelSerializer):
    # 嵌套显示商品详情，方便前端展示图片和价格
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'