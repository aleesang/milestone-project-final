from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from products.models import Product

# Create your models here.


class Order(models.Model):
    full_name = models.CharField(max_length=50, blank=True, default=None)
    email = models.EmailField(max_length=254, blank=True, default=None)
    phone_number = models.CharField(max_length=20, blank=True, default=None)
    street_address = models.CharField(max_length=100, default=None)
    address2 = models.CharField(max_length=100, blank=True, default=None, null=True)
    country = CountryField(multiple=False, default=None)
    town_or_city = models.CharField(max_length=100, default=None)
    postcode = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)

    def __str__(self):
        return "".format(self.quantity, self.product.productname, 0.1)
    
