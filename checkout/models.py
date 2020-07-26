from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from products.models import Product

# Create your models here.


class Order(models.Model):
    full_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(max_length=254, null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(multiple=False, null=True, blank=True, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)

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
    item_total = models.DecimalField(max_digits=6, decimal_places=2, default=None, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    
