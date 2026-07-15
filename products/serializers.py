from rest_framework import serializers
from .models import Product, Category, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=[
            "id",
            "name",
            "slug",
        ]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields = [
            "id",
            "name",
            "slug",
        ]

class ProductSerializer(serializers.ModelSerializer):
    brand=BrandSerializer(read_only=True)
    category=CategorySerializer(read_only=True)
    class Meta:
        model=Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "brand",
        ]