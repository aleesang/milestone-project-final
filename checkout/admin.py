from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)
    
    readonly_fields = (
            'order_number', 
            'date',
            'full_name',
            'order_total', 
            'delivery_cost',
            'final_total',
            'original_bag',
            'stripe_pid')
    
    fields = (
            'order_number',
            'user_profile',
            'date',
            'full_name', 
            'email', 
            'phone_number',
            'street_address', 
            'address2',
            'country', 
            'town_or_city', 
            'postcode',
            'order_total',  
            'delivery_cost',
            'final_total',
            'original_bag',
            'stripe_pid') 

    list_display = (
            'order_number',
            'date', 
            'full_name',
            'order_total', 
            'delivery_cost',
            'final_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)