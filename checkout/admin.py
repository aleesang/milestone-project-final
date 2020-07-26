from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)
    readonly_fields = ('order_number',)
    fields = ('order_number',
              'full_name', 
              'email', 
              'phone_number',
              'street_address', 
              'address2',
              'country', 
              'town_or_city', 
              'postcode',) 

list_display = ('order_number',)

admin.site.register(Order, OrderAdmin)