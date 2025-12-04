from django.db import models
from django.contrib.auth.models import User


# ============================
# 1. 商品分类表 (之前丢失的部分)
# ============================
class Category(models.Model):
    name = models.CharField("分类名称", max_length=50)
    icon = models.CharField("图标链接", max_length=200, default="/static/logo.png")
    sort = models.IntegerField("排序", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name


# ============================
# 2. 商品表
# ============================
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="所属分类", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="纸品名称")
    spec = models.CharField(max_length=50, verbose_name="规格", default="箱")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价(元)")
    original_price = models.DecimalField("原价", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=100, verbose_name="库存")
    image_url = models.CharField(max_length=500, verbose_name="图片链接", default="", blank=True)
    sales = models.IntegerField("销量", default=0)
    is_active = models.BooleanField(default=True, verbose_name="是否上架")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = verbose_name


# ============================
# 3. 订单表
# ============================
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', '待付款/待发货'),
        ('shipped', '已发货/配送中'),
        ('completed', '已完成'),
    )
    customer_name = models.CharField(max_length=100, verbose_name="客户信息")
    customer_phone = models.CharField(max_length=20, verbose_name="联系电话", default="")
    address = models.TextField(verbose_name="送货地址", default="")
    items_info = models.TextField(verbose_name="购买详情")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")

    def __str__(self):
        return f"{self.customer_name} - {self.total_price}"

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


# ============================
# 4. 购物车表
# ============================
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.IntegerField("数量", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name