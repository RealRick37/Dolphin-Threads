from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import ProductVariant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.decorators.http import require_POST
# Create your views here.

@login_required
@require_POST
def add_to_cart(request, variant_id):
    variant=get_object_or_404(ProductVariant, id=variant_id)

    if variant.stock <=0:
        return JsonResponse({"success": False, "message": "موجودی کافی نیست"})

    cart, created=Cart.objects.get_or_create(user=request.user)
    item, created=CartItem.objects.get_or_create(cart=cart, variant=variant)

    if not created:
        if item.quantity>=variant.stock:
            return JsonResponse({"success": False, "message": "موجودی کافی نیست"})
    
        item.quantity+=1
        item.save()

    cart_count=sum(item.quantity for item in cart.items.all())

    return JsonResponse({"success": True, "message": "محصول اضافه شد", "cart_count": cart_count})

class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name="cart_detail.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["cart"]=(Cart.objects.filter(user=self.request.user).first())

        return context
    


class RemoveFromCart(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item=get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.success(request, "محصول حذف شد.")
        return redirect("cart_detail")


class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if item.quantity < item.variant.stock:
            item.quantity += 1
            item.save()
        else:
            messages.error(request, "موجودی کافی نیست")
        return redirect("cart_detail")


class DecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
        return redirect("cart_detail")



@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        messages.error(request, "سبد خرید خالی است.")
        return redirect("cart_detail")

    if not cart.items.exists():
        messages.error(request, "سبد خرید خالی است.")
        return redirect("cart_detail")

    for item in cart.items.all():

        if item.quantity > item.variant.stock:

            messages.error(request, f"موجودی {item.variant.product.name} کافی نیست.")

            return redirect("cart_detail")
    with transaction.atomic():
        order = Order.objects.create(user=request.user, is_paid=False)

        for item in cart.items.all():

            OrderItem.objects.create(order=order, variant=item.variant, quantity=item.quantity, price=item.variant.product.price)
            item.variant.stock -= item.quantity
            item.variant.save()

        cart.items.all().delete()

        messages.success(request, "سفارش شما با موفقیت ثبت شد.")
        return redirect("order_detail", order_id=order.id)

class OrderHistoryView(LoginRequiredMixin, ListView):
    model=Order
    template_name="order_history.html"
    context_object_name="orders"

    def get_queryset(self):
        return (Order.objects.filter(user=self.request.user).order_by("-created_at"))


class OrderDetailView(LoginRequiredMixin, DetailView):
    model=Order
    template_name="order_detail.html"
    context_object_name="order"
    pk_url_kwarg = "order_id"

    def get_queryset(self):
        return (Order.objects.filter(user=self.request.user))


class AjaxIncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if item.quantity < item.variant.stock:
            item.quantity += 1
            item.save()
            return JsonResponse({"success": True, "quantity": item.quantity, "total_price": item.cart.total_price,})

        return JsonResponse({"success": False, "message": "موجودی کافی نیست"})

class AjaxDecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity -= 1
        if item.quantity <= 0:
            cart = item.cart
            item.delete()

            return JsonResponse({"success": True, "deleted": True, "total_price": cart.total_price,})
        item.save()

        return JsonResponse({"success": True, "deleted": False, "quantity": item.quantity, "total_price": item.cart.total_price,})

class AjaxRemoveItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = item.cart
        item.delete()

        return JsonResponse({"success": True, "total_price": cart.total_price,})