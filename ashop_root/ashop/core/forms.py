from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0}),  # Ensure quantity cannot be negative
        }