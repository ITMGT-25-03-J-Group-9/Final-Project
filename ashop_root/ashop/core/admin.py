from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Product, CartItem, Transaction, LineItem
from .forms import ProductForm

# Register your models here.

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
