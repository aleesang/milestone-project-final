from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()
    

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False, default=True)
    full_name = models.CharField(max_length=50, null=False, blank=False, default=True)
    email = models.EmailField(max_length=254, null=False, blank=False, default=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False, default=True)
    street_address = models.CharField(max_length=100, default=True)
    address2 = models.CharField(max_length=100, default=True)
    country = CountryField(multiple=False, default=True)
    town_or_city = models.CharField(max_length=100, default=True)
    postcode = models.CharField(max_length=100, default=True)
    items = models.ManyToManyField(OrderItem)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update final total each time a line item is added,
        accounting for delivery prices.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_price = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_price = 0
        self.final_total = self.order_total + self.delivery_price
        self.save()

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
    
class CheckoutAddress(models.Model):
    full_name = models.CharField(max_length=50, null=False, blank=False, default=True)
    email = models.EmailField(max_length=254, null=False, blank=False, default=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False, default=True)
    street_address = models.CharField(max_length=100, default=True)
    address2 = models.CharField(max_length=100, default=True)
    country = CountryField(multiple=False, default=True)
    town_or_city = models.CharField(max_length=100, default=True)
    postcode = models.CharField(max_length=100, default=True)

    def __str__(self):
        return self.user.username