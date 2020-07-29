from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    """
    The Order model stores information about the user's name,
    phone number and address  to assist in the delivery of products
    """
    order_number = models.CharField(max_length=32, null=True, blank=True, default=None, editable=False)
    full_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(max_length=254, null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(multiple=False, null=True, blank=True, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)
    date = models.DateTimeField(null=True, default=None)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
        def save(self, *args, **kwargs):
            """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False, default=None)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'