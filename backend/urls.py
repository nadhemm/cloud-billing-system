from django.urls import path

from backend.views import PushMeteringQuantity, CustomerView, SingleCustomerView, ProductView, SingleProductView, \
    PricingView, SinglePricingView

urlpatterns = [
    path('push-metering-quantity/', PushMeteringQuantity.as_view()),

    path('customers/', CustomerView.as_view()),
    path('customers/<uuid:customer_id>', SingleCustomerView.as_view()),

    path('products/', ProductView.as_view()),
    path('products/<uuid:product_id>', SingleProductView.as_view()),

    path('pricings/', PricingView.as_view()),
    path('pricings/<uuid:pricing_id>', SinglePricingView.as_view()),
]
