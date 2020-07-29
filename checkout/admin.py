from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)
    
    readonly_fields = ('order_number', 
                'date',
                'full_name',
                'order_total', 
                'delivery_cost',
                'final_total',)
    
    fields = ('order_number',
              'date',
              'full_name', 
              'email', 
              'phone_number',
              'street_address', 
              'address2',
              'country', 
              'town_or_city', 
              'postcode', 
              'delivery_cost',
              'order_total', 
              'final_total',) 

list_display = ('order_number',
                'date', 
                'full_name',
                'order_total', 
                'delivery_cost',
                'final_total',)

admin.site.register(Order, OrderAdmin)