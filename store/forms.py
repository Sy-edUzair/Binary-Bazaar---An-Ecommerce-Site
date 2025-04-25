from django import forms
from .models import *

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields=['name','description','image','address','contact']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name/Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description of Shop'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Contact'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['text','rating',]
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Your Review'}),
            'rating': forms.Select(attrs={'class': 'custom-select'}),
        }

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=['title', 'price', 'image','description','tags', 'category','in_stock','is_digital' ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter product title'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter product description',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'custom-select'
            }),
            'in_stock': forms.CheckboxInput(attrs={
                'label': 'In Stock'
            }),
            'is_digital': forms.CheckboxInput(attrs={
                'label': 'Is Digital'
            }),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model=ShippingAddress
        fields=['address','city','state','zipcode','Country' ]
        widgets={
            'address':forms.TextInput(attrs={
                'placeholder':'Enter Shipping Address'
            }),
            'city':forms.TextInput(attrs={
                'placeholder':'City'
            }),
            'state':forms.TextInput(attrs={
                'placeholder':'State'
            }),
            'zipcode':forms.TextInput(attrs={
                'placeholder':'Zipcode/Postalcode'
            }),
            'Country':forms.TextInput(attrs={
                'placeholder':'Country'
            }),
        }