from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import StockTransaction
from .serializers import StockTransactionSerializer
from products.models import Product


class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.select_related(
        'product'
    ).all().order_by('-date')

    serializer_class = StockTransactionSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.select_for_update().get(
            id=serializer.validated_data['product'].id
        )

        transaction_type = serializer.validated_data['transaction_type']
        quantity = serializer.validated_data['quantity']

        # Quantity must be positive
        if quantity <= 0:
            return Response(
                {
                    'error': 'Quantity must be greater than 0'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Stock IN
        if transaction_type == 'IN':
            product.quantity += quantity
            product.save()

        # Stock OUT
        elif transaction_type == 'OUT':

            if quantity > product.quantity:
                return Response(
                    {
                        'error': 'Not enough stock',
                        'available_stock': product.quantity,
                        'requested_quantity': quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            product.quantity -= quantity
            product.save()

        # Save transaction
        stock_transaction = serializer.save()

        return Response(
            self.get_serializer(stock_transaction).data,
            status=status.HTTP_201_CREATED
        )


from django.shortcuts import render

# Create your views here.
