from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
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