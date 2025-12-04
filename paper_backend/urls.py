from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ProductViewSet, OrderViewSet, CategoryViewSet, CartViewSet, register, login_view, AddressViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet) # 👈 这一行之前丢了，现在补上
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'addresses', AddressViewSet, basename='address') # 新增这一行

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register),
    path('api/login/', login_view),
]