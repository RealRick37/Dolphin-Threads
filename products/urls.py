from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/",ProductListView.as_view(), name="product_list"),
    path("ajax/search/", AjaxSearchProductsView.as_view(), name="ajax_search_products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/wishlist/", ToggleWishList.as_view(), name="toggle_wishlist"),
    path("wishlist/", WishlistView.as_view(), name="wishlist_detail"),
    path("products/<int:pk>/comment/add/", AddCommentView.as_view(), name="add_comment"),
    path("comments/<int:comment_id>/edit/", EditCommentView.as_view(),name="edit_comment"),
    path("comments/<int:comment_id>/delete/", DeleteCommentView.as_view(), name="delete_comment"),
    
    ]