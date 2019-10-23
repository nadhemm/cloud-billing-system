import uuid

from django.db import models
from django.db.models import Model

from backend.enum import AccountStatus


class Customer(Model):
    customer_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(blank=False, null=False, max_length=60)
    financial_consumption_amount = models.DecimalField(max_digits=15, decimal_places=10, default=0)  # to handle very small CHF amounts
    account_status = models.CharField(choices=AccountStatus.get_choices(), max_length=20)

    def __str__(self):
        return self.name


class Product(Model):
    product_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(blank=False, null=False, max_length=50)
    billable_items = models.ManyToManyField('BillableItem')

    def __str__(self):
        return self.name


class BillableItem(Model):
    item_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(blank=False, null=False, max_length=50)

    def __str__(self):
        return self.name


class Pricing(Model):
    pricing_id = models.UUIDField(unique=True, default=uuid.uuid4)
    billable_item = models.ForeignKey(BillableItem, null=False, blank=False, on_delete=models.CASCADE,
                                      related_name='pricings')
    price = models.DecimalField(max_digits=15, decimal_places=10)
    account_status = models.CharField(choices=AccountStatus.get_choices(), max_length=20)

    def __str__(self):
        return "{} {}".format(self.billable_item, self.account_status)


class ProductSubscription(Model):
    """
    we assume that a single customer can subscribe to the same product more than once
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subscription_date = models.DateField(auto_now_add=True)  # TBD, This could be used to add an expiry date..

    def __str__(self):
        return "{} {}".format(self.customer, self.product)
