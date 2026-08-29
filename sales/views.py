from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Sale
from .serializers import SaleSerializer
from .forms import SaleForm
from products.models import Product


# -----------------------
# Sales List
# -----------------------

def sale_list(request):
    sales = Sale.objects.select_related('product').order_by('-sale_date')

    return render(
        request,
        'sale_list.html',
        {
            'sales': sales
        }
    )


# -----------------------
# Add Sale
# -----------------------

@transaction.atomic
def add_sale(request):

    if request.method == 'POST':

        form = SaleForm(request.POST)

        if form.is_valid():

            sale = form.save(commit=False)

            product = Product.objects.select_for_update().get(
                id=sale.product.id
            )

            if sale.quantity > product.quantity:

                messages.error(
                    request,
                    f'Not enough stock! Available stock: {product.quantity}'
                )

                return render(
                    request,
                    'add_sale.html',
                    {'form': form}
                )

            product.quantity -= sale.quantity
            product.save()

            sale.save()

            messages.success(
                request,
                'Sale added successfully and stock updated!'
            )

            return redirect('sale_list')

    else:
        form = SaleForm()

    return render(
        request,
        'add_sale.html',
        {
            'form': form
        }
    )


# -----------------------
# REST API
# -----------------------

class SaleViewSet(viewsets.ModelViewSet):

    queryset = Sale.objects.select_related(
        'product'
    ).all().order_by('-sale_date')

    serializer_class = SaleSerializer

    # -----------------------
    # Create Sale through API
    # -----------------------

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product'].id
        sale_quantity = serializer.validated_data['quantity']

        product = Product.objects.select_for_update().get(
            id=product_id
        )

        # Check stock
        if sale_quantity > product.quantity:

            return Response(
                {
                    'error': 'Not enough stock',
                    'available_stock': product.quantity,
                    'requested_quantity': sale_quantity
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reduce stock
        product.quantity -= sale_quantity
        product.save()

        # Save sale
        sale = serializer.save()

        return Response(
            self.get_serializer(sale).data,
            status=status.HTTP_201_CREATED
        )