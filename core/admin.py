from django.contrib import admin
from .models import Product, Order, Category, CartItem

# 1. 分类管理
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')
    ordering = ('sort',)

# 2. 商品管理
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'sales', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    list_editable = ('stock', 'price', 'is_active')

# 3. 订单管理 (修复了字段名错误)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # ⚠️ 注意这里：把 phone 改成了 customer_phone
    list_display = ('id', 'customer_name', 'customer_phone', 'items_info', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    # ⚠️ 这里也改了
    search_fields = ('customer_name', 'customer_phone', 'address')
    list_editable = ('status',)

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = '当前状态'

# 4. 购物车管理
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')