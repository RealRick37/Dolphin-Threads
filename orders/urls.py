from django.urls import path
from .views import *
urlpatterns = [
    path("add/<int:variant_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_detail, name="cart_detail"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("increase/<int:item_id>/", increase_quantity, name="increase_quantity"),
    path("decrease/<int:item_id>/", decrease_quantity, name="decrease_quantity"),
    path("checkout/", checkout, name="checkout"),
    path("history/", order_history, name="order_history"),
    path("detail/<int:order_id>", order_detail, name="order_detail"),
    path("ajax/add/<int:variant_id>/", ajax_add_to_cart, name="ajax_add_to_cart"),
    path("ajax/increase/<int:item_id>/", ajax_increase_quantity, name="ajax_increase_quantity"),
    path("ajax/decrease/<int:item_id>/", ajax_decrease_quantity, name="ajax_decrease_quantity"),
    path("ajax/remove/<int:item_id>/",ajax_remove_item, name="ajax_remove_item"),
]
