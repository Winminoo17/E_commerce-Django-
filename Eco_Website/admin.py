from django.contrib import admin # type: ignore
from .models import Category, Product, Customer, Order, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    inlines = [ProfileInline]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)