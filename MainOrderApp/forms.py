from django import forms
from .models import Product
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)


class PurchaseItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select a product")
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(min_value=0, decimal_places=2)