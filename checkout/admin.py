from django.contrib import admin
from .models import Order, OrderItem

class OrderAdminInLine(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInLine, )

admin.site.register(Order, OrderAdmin)