from django import forms
from .models import Sale


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = ['customer_name', 'product', 'quantity']

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),

            'product': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Enter quantity'
            }),
        }