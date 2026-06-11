from django.shortcuts import render, redirect
from products.models import Product
from .forms import ProductForm


def dashboard(request):
    total_products = Product.objects.count()

    context = {
        'total_products': total_products,
    }

    return render(request, 'dashboard.html', context)


def product_list(request):
    products = Product.objects.all()

    return render(request, 'product_list.html', {
        'products': products
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()

    return redirect('product_list')