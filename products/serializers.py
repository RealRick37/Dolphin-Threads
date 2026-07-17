from rest_framework import serializers
from .models import Product, Category, Brand, Color, ProductVariant, ProductImage, Comment, Wishlist
from django.db.models import Avg

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

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields=[
            "id",
            "name",
        ]

class ProductVariantSerializer(serializers.ModelSerializer):
    color=ColorSerializer(read_only=True)
    class Meta:
        model=ProductVariant
        fields=[
            "id",
            "size",
            "stock",
            "color",
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=[
            "id",
            "image",
            "alt_text",
            "is_main",
        ]

class CommentSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Comment
        fields=[
            "id",
            "user",
            "product",
            "text",
            "rating",
            "created_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    brand=BrandSerializer(read_only=True)
    category=CategorySerializer(read_only=True)
    variants=ProductVariantSerializer(many=True, read_only=True)
    images=ProductImageSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    class Meta:
        model=Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "brand",
            "variants",
            "images",
            "avg_rating",
            "comment_count",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)

    class Meta:
        model=Wishlist
        fields=[
            "id",
            "product",
            "created_at",
        ]

class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields=[
            "product",
        ]