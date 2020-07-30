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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', null=True, default=None, editable=False)
    order_number = models.CharField(max_length=32, null=True, default=None, editable=False)
    full_name = models.CharField(max_length=50, null=True, blank=False, default=None)
    email = models.EmailField(max_length=254, null=True, blank=False, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=False, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=False, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(multiple=False, null=True, blank=False, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)
    date = models.DateTimeField(null=True, default=None)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False, default=None)

    def __str__(self):
        return "{0} {1} @ {2}".format(
            self.quantity, self.product.name, self.product.price)