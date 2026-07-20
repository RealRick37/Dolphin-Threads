from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="variant.product.name", read_only=True)
    size=serializers.CharField(source="variant.size", read_only=True)
    color=serializers.CharField(source="variant.color.name", read_only=True)

    class Meta:
        model=CartItem
        fields=[
            "id",
            "quantity",
            "product_name",
            "size",
            "color",
        ]

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True, read_only=True)
    total_price=serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model=Cart
        fields=[
            "id",
            "items",
            "total_price",
            "created_at",
        ]

class AddToCartSerializer(serializers.Serializer):
    variant_id=serializers.IntegerField()
    quantity=serializers.IntegerField(default=1)


class OrderItemSerializer(serializers.ModelSerializer):
    variant=ProductVariantSerializer(read_only=True)

    class Meta:
        model=OrderItem
        fields=[
            "id",
            "variant",
            "quantity",
            "price",
        ]

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True ,read_only=True)

    class Meta:
        model=Order
        fields=[
            "id",
            "status",
            "is_paid",
            "created_at",
            "items",
        ]