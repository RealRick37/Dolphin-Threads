from django.urls import path
from .views import *
urlpatterns = [
    path("add/<int:variant_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
    path("remove/<int:item_id>/", RemoveFromCart.as_view(), name="remove_from_cart"),
    path("increase/<int:item_id>/", IncreaseQuantityView.as_view(), name="increase_quantity"),
    path("decrease/<int:item_id>/", DecreaseQuantityView.as_view(), name="decrease_quantity"),
    path("checkout/", checkout, name="checkout"),
    path("history/", OrderHistoryView.as_view(), name="order_history"),
    path("detail/<int:order_id>", OrderDetailView.as_view(), name="order_detail"),
    path("ajax/increase/<int:item_id>/", AjaxIncreaseQuantityView.as_view(), name="ajax_increase_quantity"),
    path("ajax/decrease/<int:item_id>/", AjaxDecreaseQuantityView.as_view(), name="ajax_decrease_quantity"),
    path("ajax/remove/<int:item_id>/",AjaxRemoveItemView.as_view(), name="ajax_remove_item"),
]
