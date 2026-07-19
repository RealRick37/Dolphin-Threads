from django.urls import path
from .api_views import (CartAPIView, AddToCartAPIView, IncreaseCartItemAPIView, DecreaseCartItemAPIView, RemoveCartItemAPIView,
                         CheckoutAPIView, OrderHistoryAPIView, OrderDetailAPIView)

urlpatterns =[
    path("cart/", CartAPIView.as_view(), name="api_cart"),
    path("cart/add/", AddToCartAPIView.as_view(), name="api_add_to_cart"),
    path("cart/item/<int:item_id>/increase/", IncreaseCartItemAPIView.as_view(), name="api_increase_cart_item"),
    path("cart/item/<int:item_id>/decrease/", DecreaseCartItemAPIView.as_view(), name="api_deccrease_cart_item"),
    path("cart/item/<int:item_id>/remove/", RemoveCartItemAPIView.as_view(), name="api_remove_cart_item"),
    path("checkout/", CheckoutAPIView.as_view(), name="api_checkout"),
    path("orders/", OrderHistoryAPIView.as_view(), name="api_order_history"),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="api_order_detail"),
]