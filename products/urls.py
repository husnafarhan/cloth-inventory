from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    dashboard,
    product_list,
    add_product,
    edit_product,
    delete_product,
    ProductViewSet,
)

router = DefaultRouter()

router.register(
    r'api/products',
    ProductViewSet,
    basename='product'
)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/edit/<int:id>/', edit_product, name='edit_product'),
    path('products/delete/<int:id>/', delete_product, name='delete_product'),

    # REST API
    path('', include(router.urls)),
]