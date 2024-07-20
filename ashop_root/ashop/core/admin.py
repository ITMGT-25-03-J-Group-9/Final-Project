from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Product, CartItem, Transaction, LineItem, Size
from .forms import ProductForm

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_sizes', 'price', 'quantity', 'image')
	fields = ('name', 'size', 'price', 'quantity', 'image',) 
	form = ProductForm
	search_fields = ('name',) 
	list_filter = ('price',)

	def display_sizes(self, obj):
		return ", ".join([size.size_name for size in obj.size.all()])		
	display_sizes.short_description = 'Sizes'

class CartItemAdmin(admin.ModelAdmin):
	list_display = ('user', 'product', 'size', 'quantity')
	list_filter = ('user', 'product', 'size')

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at')
	list_filter = ('user', 'created_at')

class LineItemAdmin(admin.ModelAdmin):
	list_display = ('transaction', 'product', 'size', 'quantity')
	list_filter = ('transaction', 'product', 'size')

class SizeAdmin(admin.ModelAdmin):
	list_display = ('size_code', 'size_name')

admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Size, SizeAdmin)
