from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 引入所有需要的 ViewSet
from core.views import ProductViewSet, OrderViewSet, CartViewSet, register, login_view

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

# ⚠️⚠️⚠️ 关键修改在这里：必须加上 basename='cart' ⚠️⚠️⚠️
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # 注册登录
    path('api/register/', register),
    path('api/login/', login_view),
]