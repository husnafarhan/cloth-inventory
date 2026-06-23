from django.shortcuts import render, redirect
from products.models import Product
from .forms import ProductForm


# Dashboard
def dashboard(request):

    products = Product.objects.all()

    total_products = products.count()

    total_stock = sum(product.quantity for product in products)

    total_value = sum(
        product.quantity * product.selling_price
        for product in products
    )

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'total_value': total_value,
    }

    return render(request, 'dashboard.html', context)


# Product List
def product_list(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'product_list.html', {
        'products': products
    })


# Add Product
def add_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {
        'form': form
    })


# Edit Product
def edit_product(request, id):

    product = Product.objects.get(id=id)

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )


        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form
    })


# Delete Product
def delete_product(request, id):

    product = Product.objects.get(id=id)

    product.delete()

    return redirect('product_list')