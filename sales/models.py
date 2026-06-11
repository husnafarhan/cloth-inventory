from django.db import models
from products.models import Product


class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name