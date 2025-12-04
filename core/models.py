from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="纸品名称")
    spec = models.CharField(max_length=50, verbose_name="规格", default="箱")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价(元)")
    stock = models.IntegerField(default=100, verbose_name="库存")
    # 为了演示简单，先用图片链接，后面教你改上传
    image_url = models.TextField(verbose_name="图片链接", default="https://via.placeholder.com/150")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = verbose_name

class Order(models.Model):
    STATUS_CHOICES = (
        (0, '待付款'),
        (1, '已接单/配送中'),
        (2, '已完成'),
    )
    customer_name = models.CharField(max_length=50, verbose_name="客户姓名")
    phone = models.CharField(max_length=20, verbose_name="电话")
    address = models.TextField(verbose_name="地址")
    items_info = models.TextField(verbose_name="购买清单") # 存类似 "卷纸x2, 抽纸x1"
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")

    class Meta:
        verbose_name = "订单中心"
        verbose_name_plural = verbose_name


# ============================
# 4. 购物车表 (新增)
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