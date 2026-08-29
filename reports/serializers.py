from rest_framework import serializers


class ReportsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_stock = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    total_sales = serializers.IntegerField()
    total_sales_quantity = serializers.IntegerField()