from django.contrib import admin
from .models import Product, Order, Category, CartItem, Address


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


# 3. 订单管理
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 👇 关键修改：我把 'address' 加到了第 4 个位置，这样列表直接显示地址！
    list_display = (
    'id', 'customer_name', 'customer_phone', 'address', 'items_info', 'total_price', 'status', 'created_at')

    # 右侧过滤器
    list_filter = ('status', 'created_at')

    # 搜索框：允许搜名字、电话、地址
    search_fields = ('customer_name', 'customer_phone', 'address')

    # 在列表页直接修改状态（方便你快速点发货）
    list_editable = ('status',)

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = '当前状态'

# 4. 购物车管理
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')

# 5. 收货地址管理 (这是新加的，让你能看到所有人的地址库)
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'street', 'is_default')
    search_fields = ('name', 'phone', 'street')
    list_filter = ('is_default',)