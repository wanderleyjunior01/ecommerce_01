from django.urls import path
from .views import (item_list, HomeView, ProductDetailView, OrderSummaryView, CheckOutView, add_to_cart, remove_from_cart, 
                        remove_single_from_cart)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="item_list"),
    path("product/<slug>/", ProductDetailView.as_view(), name="product"),
    path("add_cart/<slug>", add_to_cart, name="add_to_cart"),
    path("remove_cart/<slug>", remove_from_cart, name="remove_from_cart"),
    path("order_summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("remove_single_cart/<slug>", remove_single_from_cart, name="remove_single_item_from_cart"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
]