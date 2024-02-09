from django.contrib import admin
from .models import Product, SaleInvoice, SoldItem, PurchaseInvoice, PurchasedItem

admin.site.register(Product)
admin.site.register(SaleInvoice)
admin.site.register(SoldItem)
admin.site.register(PurchaseInvoice)
admin.site.register(PurchasedItem)


