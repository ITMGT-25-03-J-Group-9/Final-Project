from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.IntegerField()
	image = models.ImageField(upload_to='product_images/', blank=True, null=True)
	quantity = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name

class CartItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
	quantity = models.IntegerField()
	def __str__(self):
		return f'{self.quantity} of {self.product} (User: {self.user.username})'

class Transaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	created_at = models.DateTimeField()

	def __str__(self):
		return f'Transaction {self.id} by {self.user.username} on {self.created_at}'

	def delete(self, *args, **kwargs):
		line_items = LineItem.objects.filter(transaction=self)
        
		for line_item in line_items:
			product = line_item.product
			product.quantity += line_item.quantity  # Re-add the quantity
			product.save()
        
		super().delete(*args, **kwargs)	

class LineItem(models.Model):
	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
	quantity = models.IntegerField()

	def __str__(self):
		return f'{self.quantity} of {self.product} in Transaction {self.transaction.id}'