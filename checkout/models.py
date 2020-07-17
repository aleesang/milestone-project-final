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

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_bag_url(self):
        return reverse("core:add-to-bag", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_bag_url(self):
        return reverse("core:remove-from-bag", kwargs={
            "pk" : self.pk
        })

    def __str__(self):
        return self.order_number

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_bag_url(self):
        return reverse("core:add-to-bag", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_bag_url(self):
        return reverse("core:remove-from-bag", kwargs={
            "pk" : self.pk
        })

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
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
class CheckoutAddress(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    post_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username