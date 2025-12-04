from django.contrib import admin
from .models import Product, Order, CartItem


# 注册商品表
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 列表页显示哪些字段
    list_display = ('name', 'spec', 'price', 'stock', 'is_active')
    # 允许搜索的字段
    search_fields = ('name',)

# 注册订单表
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'total_price', 'status', 'created_at')
    # 右侧增加过滤器（按状态筛选）
    list_filter = ('status',)
    search_fields = ('customer_name', 'phone')

# 4. 购物车管理 (新增的部分)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name') # 支持搜用户名和商品名