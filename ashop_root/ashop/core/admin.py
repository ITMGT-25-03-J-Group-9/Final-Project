from django.contrib import admin

from .models import Product
from .models import CartItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'image')  # Display fields in the list view
	fields = ('name', 'price', 'image')  # Fields to display on the form page

admin.site.register(Product, ProductAdmin)
