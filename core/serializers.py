from rest_framework import serializers
from .models import Product, Order, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    # 为了让前端能直接显示商品名和图片，我们需要嵌套商品详情
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'quantity', 'product_detail']