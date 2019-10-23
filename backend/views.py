import logging
from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import ProductSubscription, Product, Customer, BillableItem, Pricing
from backend.serializers import CustomerSerializer, ProductSerializer, PricingSerializer

logger = logging.getLogger(__name__)


class PushMeteringQuantity(APIView):

    def post(self, request):
        try:
            product_id = UUID(request.data.get('product_id', ""), version=4)
        except ValueError:
            logger.warning("Invalid product UUID %s", request.data.get('product_id'))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(product_id=product_id)
        except ObjectDoesNotExist:
            logger.warning("Product with id %s does not exist.", product_id)
            return Response(status=status.HTTP_404_NOT_FOUND)
        subscriptions = ProductSubscription.objects.filter(product=product)
        try:
            for billable_item in product.billable_items.all():
                for subscription in subscriptions:
                    customer = subscription.customer
                    amount = \
                    billable_item.pricings.filter(account_status=customer.account_status).aggregate(Sum('price'))[
                        'price__sum']
                    if type(amount) != Decimal:
                        logger.warning("No pricing available for this item %s with this account status %s",
                                       billable_item, customer.account_status)
                        continue
                    customer.financial_consumption_amount += amount
                    customer.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("A server exception occurred \nError details: %s", e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleCustomerView(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'customer_id'


class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleProductView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'


class PricingView(ListCreateAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer

    def perform_create(self, serializer):
        billable_item = get_object_or_404(BillableItem, item_id=self.request.data.get('billable_item_id'))
        return serializer.save(billable_item=billable_item)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SinglePricingView(RetrieveUpdateDestroyAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    lookup_field = 'pricing_id'
