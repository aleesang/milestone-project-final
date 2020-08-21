from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from products.models import Product
from django.contrib.auth.models import User
from profiles.models import Profile

# Create your models here.


class Order(models.Model):
    """
    The Order model stores information about the user's name,
    phone number and address  to assist in the delivery of products
    """
    order_number = models.CharField(max_length=32, null=True, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=True, blank=False, default=None)
    email = models.EmailField(max_length=254, null=True, blank=False, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=False, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=False, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(blank_label='Country *', multiple=False, null=False, blank=False, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)
    date = models.DateTimeField(null=True, default=None)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)
    
        def update_total(self):
            """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.DELIVERY_DISCOUNT:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.final_total = self.order_total + self.delivery_cost
        self.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False, default=None)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the item total
        and update the order total.
        """
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'