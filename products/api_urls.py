from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, CommentViewSet, ProductCommentsAPIView, WishlistViewSet
from django.urls import path

router=DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("comments", CommentViewSet, basename="comment")
router.register("wishlist", WishlistViewSet, basename="wishlist")

urlpatterns=router.urls

urlpatterns += [
    path("products/<int:product_id>/comments/", ProductCommentsAPIView.as_view(), name="product_comments"),
]

