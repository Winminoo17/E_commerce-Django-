from django.db import models # type: ignore
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank = True)
    address1 = models.CharField(max_length=50, blank = True)
    address2 = models.CharField(max_length=50, blank = True)
    state = models.CharField(max_length=50, blank = True)
    city = models.CharField(max_length=50, blank = True)
    zipcode = models.CharField(max_length=50, blank = True)
    country = models.CharField(max_length=50, blank = True)
    old_cart = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f' {self.user.username} '
    
def  create_profile(sender, instance, created, **kwargs):
     if created:
         user_profile = Profile(user=instance)
         user_profile.save()
post_save.connect(create_profile, sender=User)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f' {self.name} '
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f' {self.name} '
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=20, default='', blank=True)
    address = models.CharField(max_length=100, default='', blank=True)
    status = models.BooleanField(default=False)
    data = models.DateField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.product
    
