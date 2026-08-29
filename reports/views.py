from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product
from sales.models import Sale

from .serializers import ReportsSerializer


class ReportsAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        sales = Sale.objects.all()

        total_products = products.count()

        total_stock = sum(
            product.quantity
            for product in products
        )

        total_stock_value = sum(
            product.quantity * product.selling_price
            for product in products
        )

        total_sales = sales.count()

        total_sales_quantity = sum(
            sale.quantity
            for sale in sales
        )

        data = {
            'total_products': total_products,
            'total_stock': total_stock,
            'total_stock_value': total_stock_value,
            'total_sales': total_sales,
            'total_sales_quantity': total_sales_quantity,
        }

        serializer = ReportsSerializer(data)

        return Response(serializer.data)


from django.shortcuts import render

# Create your views here.
