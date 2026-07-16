from .models import Product, Comment
from .serializers import ProductSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Avg, Count, Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    permission_classes=[IsAuthenticatedOrReadOnly,    IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)