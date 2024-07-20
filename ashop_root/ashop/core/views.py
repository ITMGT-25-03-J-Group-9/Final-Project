from django.http import HttpResponse
from django.template import loader
from core.models import Product, CartItem, Transaction, LineItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import(
	login, logout, authenticate
)
from django.contrib import messages
import datetime as dt
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def index(request):
	template = loader.get_template("core/index.html")
	products = Product.objects.all()
	context = {
		"user": request.user,
		"product_data": products
	}
	return HttpResponse(template.render(context, request))

@login_required
def product_detail(request, product_id):
	if request.method == 'GET':
		template = loader.get_template("core/product_detail.html")
		p = Product.objects.get(id=product_id)
		context = {
			"product": p,
			"max_quantity": p.quantity
		}
		return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		submitted_quantity = int(request.POST['quantity'])
		submitted_product_id = request.POST['product_id']
		product = Product.objects.get(id=submitted_product_id)

		if submitted_quantity > product.quantity:
			messages.add_message(
				request,
				messages.ERROR,
				f'Cannot add more than {product.quantity} of {product.name} to your cart.'
			)
			return redirect(request.path_info)

		user = request.user
		cart_item = CartItem(user=user, product=product, quantity=submitted_quantity)
		cart_item.save()
		messages.add_message(
			request,
			messages.INFO,
			f'Added {submitted_quantity} of {product.name} to your cart'
		)
		return redirect('index')

def login_view(request):
	if request.method == 'GET':
		template = loader.get_template("core/login_view.html")
		context = {}
		return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		submitted_username = request.POST['username']
		submitted_password = request.POST['password']
		user_object = authenticate(
			username=submitted_username,
			password=submitted_password
		)
		if user_object is None:
			messages.add_message(request, messages.INFO, 'Invalid login.')
			return redirect(request.path_info)
		login(request, user_object)
		return redirect('index')

@login_required
def checkout(request):
	if request.method == 'GET':
		template = loader.get_template("core/checkout.html")
		cart_items = CartItem.objects.filter(user=request.user)
        
		total_price = 0
		for item in cart_items:
			item.total_price = item.product.price * item.quantity
			total_price += item.total_price

		context = {
			'cart_items': cart_items,
			'total_price': total_price,
		}
		return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		cart_items = CartItem.objects.filter(user=request.user)
		created_at = dt.datetime.now(tz=dt.timezone.utc)
		transaction = Transaction(user=request.user, created_at=created_at)
		transaction.save()
		for cart_item in cart_items:
			line_item = LineItem(
				transaction=transaction,
				product=cart_item.product,
				quantity=cart_item.quantity,
			)
			line_item.save()
			product = cart_item.product
			product.quantity -= cart_item.quantity
			product.save()
		
		cart_item.delete()
		messages.add_message(request, messages.INFO, f'Thank you for your purchase!')
		return redirect('index')

@login_required
def transaction_history(request):
	transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')

	for transaction in transactions:
		total_price = sum(line_item.product.price * line_item.quantity for line_item in transaction.lineitem_set.all())
		transaction.total_price = total_price

	context = {
		"transactions": transactions
	}
	return render(request, 'core/transaction_history.html', context)

@login_required
def remove_cart_item(request, cart_item_id):
	if request.method == 'POST':
		cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
		cart_item.delete()
		return redirect('checkout')
	else:
 		return redirect('checkout')

def logout_view(request):
	logout(request)
	return redirect('login_view')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Registration successful. Please log in.')
			return redirect(reverse('login_view'))
	else:
		form = UserCreationForm()

	template = loader.get_template('core/register.html')
	context = {
		'form': form,
	}
	return HttpResponse(template.render(context, request))

@staff_member_required
def inventory_view(request):
	products = Product.objects.all()
	context = {
		'products': products
	}
	return render(request, 'core/inventory.html', context)