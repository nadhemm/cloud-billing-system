from django.contrib import admin

from backend.models import Customer, Product, BillableItem, Pricing, ProductSubscription

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(BillableItem)
admin.site.register(Pricing)
admin.site.register(ProductSubscription)
