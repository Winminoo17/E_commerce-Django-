from django.contrib import admin
from .models import ShippingAddress, OrderModel, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderModel)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    model = OrderModel
    readonly_fields = ['order_date']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount_paid', 'order_date', 'shipped', 'date_ship']
    inlines = [OrderItemInline]
    
admin.site.unregister(OrderModel)
admin.site.register(OrderModel, OrderAdmin)