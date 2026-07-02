from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import ProductVariant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required
def add_to_cart(request, variant_id):
    variant=get_object_or_404(ProductVariant, id=variant_id)
    cart, created=Cart.objects.get_or_create(user=request.user)
    item, created=CartItem.objects.get_or_create(cart=cart, variant=variant)

    if variant.stock <=0:
        return JsonResponse({"success": False, "message": "موجودی کافی نیست"})

    if not created:
        if item.quantity>=variant.stock:
            return JsonResponse({"success": False, "message": "موجودی کافی نیست"})
    
        item.quantity+=1
        item.save()

    cart_count=sum(item.quantity for item in cart.items.all())

    return JsonResponse({"success": True, "message": "محصول اضافه شد", "cart_count": cart_count})

@login_required
def cart_detail(request):
    cart=Cart.objects.filter(user=request.user).first()

    return render(request, "cart_detail.html", {"cart":cart})


def remove_from_cart(request, item_id):
    item=get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "محصول حذف شد.")

    return redirect("cart_detail")


def increase_quantity(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity < item.variant.stock:
        item.quantity += 1
        item.save()
    else:
        messages.error(request, "موجودی کافی نیست")

    return redirect("cart_detail")


def decrease_quantity(request, item_id):

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

    order = Order.objects.create(user=request.user, is_paid=False)

    for item in cart.items.all():

        OrderItem.objects.create(order=order, variant=item.variant, quantity=item.quantity, price=item.variant.product.price)
        item.variant.stock -= item.quantity
        item.variant.save()

    cart.items.all().delete()

    messages.success(request, "سفارش شما با موفقیت ثبت شد.")
    return redirect("order_detail", order_id=order.id)


@login_required
def order_history(request):
    orders=Order.objects.filter(user=request.user).order_by("created_at")

    return render(request, "order_history.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order=get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "order_detail.html", {"order": order})

@login_required
def ajax_add_to_cart(request, variant_id):
    variant=get_object_or_404(ProductVariant, id=variant_id)
    cart, created=Cart.objects.get_or_create(user=request.user)
    item, created=CartItem.objects.get_or_create(cart=cart, variant=variant)

    if not created:
        item.quantity+=1
        item.save()
    cart_count=sum(i.quantity for i in cart.items.all())

    return JsonResponse({"success": True, "cart_count": cart_count})
@login_required
def ajax_increase_quantity(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity < item.variant.stock:

        item.quantity += 1
        item.save()

        return JsonResponse({"success": True, "quantity": item.quantity, "total_price": item.cart.total_price,})

    return JsonResponse({"success": False, "message": "موجودی کافی نیست"})

@login_required
def ajax_decrease_quantity(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    item.quantity -= 1

    if item.quantity <= 0:

        cart=item.cart

        item.delete()

        return JsonResponse({"success": True, "deleted": True, "total_price": cart.total_price,})

    item.save()

    return JsonResponse({"success": True, "deleted": False, "quantity": item.quantity, "total_price": item.cart.total_price,})

@login_required
def ajax_remove_item(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    cart=item.cart

    item.delete()

    return JsonResponse({"success": True, "total_price": cart.total_price,})