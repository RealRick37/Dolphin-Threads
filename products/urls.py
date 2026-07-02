from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("products/",product_list, name="product_list"),
    path("ajax/search/", ajax_search_products, name="ajax_search_products"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("products/<int:pk>/wishlist/", toggle_wishlist, name="toggle_wishlist"),
    path("wishlist/", wishlist_detail, name="wishlist_detail"),
    path("products/<int:pk>/comment/add/", add_comment, name="add_comment"),
    path("comments/<int:comment_id>/edit/", edit_comment,name="edit_comment"),
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    
    ]