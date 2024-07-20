from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Product, CartItem, Transaction, LineItem
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site
from .forms import ProductForm

# Register your models here.

class CustomAdminSite(AdminSite):
	site_header = "Custom Admin"

admin_site = CustomAdminSite(name='custom_admin')

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'quantity')
	change_list_template = 'admin/core/inventory.html'  # Use your custom template here

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('inventory/', self.admin_site.admin_view(self.inventory_view))
        	]
		return custom_urls + urls

	def inventory_view(self, request):
		context = {
			'products': Product.objects.all()
		}
		return render(request, 'admin/core/inventory.html', context)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'quantity', 'image')
	fields = ('name', 'price', 'quantity', 'image')  
	form = ProductForm
	search_fields = ('name',)
	list_filter = ('price',)

class CartItemAdmin(admin.ModelAdmin):
	list_display = ('user', 'product', 'quantity')
	list_filter = ('user', 'product')

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at')
	list_filter = ('user', 'created_at')

class LineItemAdmin(admin.ModelAdmin):
	list_display = ('transaction', 'product', 'quantity')
	list_filter = ('transaction', 'product')

admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LineItem, LineItemAdmin)
