from django.urls import path

from . import views # This . package just means "the current package; we are importing the sister file "views.py"

urlpatterns = [
	path('register/', views.register, name='register'),
	path("", views.index, name="index"),
	path("product/<int:product_id>", views.product_detail, name="product_detail"),
	path("accounts/login/", views.login_view, name="login_view"),
	path("checkout", views.checkout, name="checkout"),
	path("transaction_history/", views.transaction_history, name="transaction_history"),
	path('remove-cart-item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
	path("logout/", views.logout_view, name="logout"),
	path('inventory/', views.inventory_view, name='inventory_view'),
]