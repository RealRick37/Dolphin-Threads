from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, CommentViewSet

router=DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns=router.urls