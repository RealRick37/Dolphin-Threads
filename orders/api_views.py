from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem
from products.models import ProductVariant
from .serializers import CartSerializer, AddToCartSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

@extend_schema(summary="Get current cart", description="Returns authenticated user's cart.")
class CartAPIView(RetrieveAPIView):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        cart, created=Cart.objects.get_or_create(user=self.request.user)
        return cart

@extend_schema(summary="Add item to cart", description="Add product variant to cart.")
class AddToCartAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer=AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant_id=serializer.validated_data["variant_id"]
        quantity=serializer.validated_data["quantity"]

        variant =ProductVariant.objects.get(id=variant_id)
        cart, created=Cart.objects.get_or_create(user=request.user)
        item, created=CartItem.objects.get_or_create(cart=cart, variant=variant)

        if quantity > variant.stock:
            return Response({"detail": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        if not created:
            item.quantity+=quantity
        else:
            item.quantity=quantity

        item.save()

        return Response({"detail": "Added to cart"}, status=status.HTTP_201_CREATED)

class IncreaseCartItemAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, item_id):
        item=get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if item.quantity>=item.variant.stock:
            return Response({"detail": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        
        item.quantity+=1
        item.save()

        return Response({"quantity": item.quantity})

class DecreaseCartItemAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, item_id):
        item=get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity-=1

        if item.quantity<=0:
            item.delete()
            return Response({"deleted": True})
        item.save()

        return Response({"deleted": False, "quantity": item.quantity})

class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        item=get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return Response({"detail": "Deleted"})

@extend_schema(summary="Checkout", description="Create order from cart and reduce stock.")
class CheckoutAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        cart=Cart.objects.filter(user=request.user).first()

        if not cart:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in cart.items.all():
            if item.quantity>item.variant.stock:
                return Response({"detail": f"Not enough stock for {item.variant.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order=Order.objects.create(user=request.user, is_paid=False)

            for item in cart.items.all():
                OrderItem.objects.create(order=order, variant=item.variant, quantity=item.quantity, price=item.variant.product.price)
                item.variant.stock-=item.quantity
                item.variant.save()
            
            cart.items.all().delete()

            return Response({"detail": "Order created", "order_id": order.id})


@extend_schema(summary="Order history", description="Returns all orders of current user.")
class OrderHistoryAPIView(ListAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return(Order.objects.filter(user=self.request.user).prefetch_related("items__variant").order_by("-created_at"))

@extend_schema(summary="Order detail", description="Returns one order.")
class OrderDetailAPIView(RetrieveAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return(Order.objects.filter(user=self.request.user).prefetch_related("items__variant"))