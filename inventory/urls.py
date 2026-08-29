from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StockTransactionViewSet


router = DefaultRouter()

router.register(
    r'stock',
    StockTransactionViewSet,
    basename='stock'
)


urlpatterns = [
    path('api/', include(router.urls)),
]