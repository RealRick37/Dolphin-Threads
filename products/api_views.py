from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView 

class ProductListAPIView(APIView):
    def get(self, request):
        products=Product.objects.all()
        serializer=ProductSerializer(products, many=True)

        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=ProductSerializer(product)

        return Response(serializer.data)
    
class ProducCreateAPIView(APIView):
    def post(self, request):
        serializer=ProductSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class ProductUpdateAPIView(APIView):
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer=ProductSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    def delete(self, request, pk):
        product=get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted."}, status=status.HTTP_204_NO_CONTENT)