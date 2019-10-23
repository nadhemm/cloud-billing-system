from rest_framework import serializers

from backend.models import Product, Customer, BillableItem, Pricing


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'name', 'financial_consumption_amount', 'account_status')


class BillableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillableItem
        fields = ('item_id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    billable_items = BillableItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Product
        fields = ('product_id', 'name', 'billable_items')


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('billable_item_id', 'pricing_id', 'price', 'account_status')
