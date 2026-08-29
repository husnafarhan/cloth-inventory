from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import sale_list, add_sale, SaleViewSet


router = DefaultRouter()

router.register(
    r'sales',
    SaleViewSet,
    basename='sale'
)


urlpatterns = [
    # Sales Pages
    path('', sale_list, name='sale_list'),
    path('add/', add_sale, name='add_sale'),

    # REST API
    path('api/', include(router.urls)),
]