from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    size = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name