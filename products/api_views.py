from .models import Product, Comment, Wishlist
from .serializers import ProductSerializer, CommentSerializer, WishlistSerializer, WishlistCreateSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Avg, Count, Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.select_related("brand", "category").prefetch_related("images", "variants__color").annotate(
    avg_rating=Avg("comments__rating", filter=Q(comments__is_approved=True)), comment_count=Count("comments", filter=Q(comments__is_approved=True)))

    serializer_class=ProductSerializer
    permission_classes=[IsAdminOrReadOnly]
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,]
    
    search_fields=[
        "name",
        "brand__name",
]
    ordering_fields = [
    "price",
    "created_at",
    "name",
]
    filterset_class=ProductFilter

class CommentViewSet(ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        product=serializer.validate_data["product"]

        if Comment.objects.filter(user=self.request.user, product=product).exists():
            raise ValidationError({"detail": "شما برای این محصول نظر ثبت کرده اید."})
        
        serializer.save(user=self.request.user)

class ProductCommentsAPIView(ListAPIView):
    serializer_class=CommentSerializer

    def get_queryset(self):
        product_id=self.kwargs["product_id"]

        return Comment.objects.filter(product_id=product_id, is_approved=True).select_related("user")

class WishlistViewSet(ModelViewSet):
    serializer_class=WishlistSerializer
    permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related("product")

    def get_serializer_class(self):
        if self.action == "create":
            return WishlistCreateSerializer

        return WishlistSerializer
    
    def perform_create(self, serializer):

        product = serializer.validated_data["product"]

        if Wishlist.objects.filter(user=self.request.user, product=product).exists():
            raise ValidationError({"detail": "این محصول قبلا به علاقه مندی ها اضافه شده"})
        serializer.save(user=self.request.user)