from django.db import models
from django.contrib.auth.models import User
from Eco_Website.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    shipping_full_name = models.CharField( max_length=50)
    shipping_email = models.EmailField(max_length=50)
    shipping_address = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=50, null = True, blank = True)
    shipping_zipcode = models.CharField(max_length=50, null = True, blank = True)
    shipping_country = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Shipping Address'
        
    def __str__(self):
        return f'Shipping Address for {str(self.id)}'
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
post_save.connect(create_shipping, sender=User)
    
class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    full_name = models.CharField( max_length=50)
    email = models.EmailField(max_length=50)
    shipping_address = models.TextField(max_length=5000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_ship = models.DateTimeField(null = True, blank = True)
    
    def __str__(self):
        return f'Order for {str(self.id)}'

@receiver(pre_save, sender=OrderModel)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.date_ship:
            instance.date_ship = now
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Oder Item - {str(self.id)}'