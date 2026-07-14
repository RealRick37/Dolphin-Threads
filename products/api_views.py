from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAdminOrReadOnly]