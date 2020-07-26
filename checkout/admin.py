from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    fields = ('full_name', 
              'email', 
              'phone_number',
              'street_address', 
              'address2',
              'town_or_city', 
              'country', 
              'postcode',) 


admin.site.register(Order, OrderAdmin)