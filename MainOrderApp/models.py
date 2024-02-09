from django.db import models

from django.contrib.auth.models import User

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    currency=models.CharField(max_length=3)
    description = models.TextField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class SaleInvoice(models.Model):
    sale_invoice_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale Invoice ID: {self.sale_invoice_id}"


class SoldItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Sale Invoice {self.sale_invoice.sale_invoice_id}"

class PurchaseInvoice(models.Model):
    purchase_invoice_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase Invoice ID: {self.purchase_invoice_id}"

class PurchasedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Purchase Invoice {self.purchase_invoice.purchase_invoice_id}"