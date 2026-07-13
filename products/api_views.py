from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer