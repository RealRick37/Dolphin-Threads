from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Brand, Wishlist, Comment
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
    latest_products=Product.objects.filter(is_active=True).order_by("-created_at")[:8]
    categories=Category.objects.all()
    brands=Brand.objects.all()[:8]
    context={
        "latest_products":latest_products,
        "categories":categories,
        "brands":brands,
    }

    return render(request, "home.html", context)

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    category = request.GET.get("category")
    brand = request.GET.get("brand")
    sort = request.GET.get("sort")
    q = request.GET.get("q")

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    if category:
        products = products.filter(category__slug=category)

    if brand:
        products = products.filter(brand__slug=brand)
    
    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    categories = Category.objects.all()
    brands = Brand.objects.all()

    paginator = Paginator(products, 6)

    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "product_list.html", {"products": products, "categories": categories, "selected_category": category, "brands": brands, "sort": sort})



from django.core.paginator import Paginator
from django.db.models import Avg

def product_detail(request, pk):

    product = get_object_or_404(Product, pk=pk, is_active=True)
    approved_comments = product.comments.filter(is_approved=True)
    avg_rating = approved_comments.aggregate(Avg("rating"))["rating__avg"]
    comment_count = approved_comments.count()
    paginator = Paginator(approved_comments.order_by("-created_at"),5)
    
    page_number = request.GET.get("comment_page")
    comments = paginator.get_page(page_number)

    in_wishlist = False
    user_has_commented = False

    images = product.images.all()

    main_image = product.image

    if request.user.is_authenticated:

        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

        user_has_commented = Comment.objects.filter(user=request.user, product=product).exists()

    return render(request, "product_detail.html",
        {
            "product": product,
            "comments": comments,
            "avg_rating": avg_rating,
            "comment_count": comment_count,
            "in_wishlist": in_wishlist,
            "user_has_commented": user_has_commented,
            "images": images,
            "main_image": main_image,
        }
    )

def ajax_search_products(request):

    query = request.GET.get("q", "")

    products = Product.objects.filter(name__icontains=query, is_active=True)[:10]

    data = []

    for product in products:

        data.append({"id": product.id, "name": product.name, "price": str(product.price), "brand":product.brand.name, "image": (product.image.url if product.image else "/static/images/no-image.jpg"),})

    return JsonResponse(data, safe=False)


@login_required
@require_POST
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)

    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        in_wishlist = True
    else:
        wishlist_item.delete()
        in_wishlist = False

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({"success": True, "in_wishlist": in_wishlist, "wishlist_count": wishlist_count,})

@login_required
def wishlist_detail(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist.html", {"items": items})


@login_required
@require_POST
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        rating = request.POST.get("rating")

        if not text or not rating:
            messages.error(request, "لطفاً متن و امتیاز را وارد کنید.")
            return redirect("product_detail", pk=pk)

        if Comment.objects.filter(user=request.user, product=product).exists():
            messages.warning(request, "شما قبلاً نظر خود را ثبت کرده‌اید.")
            return redirect("product_detail", pk=pk)
        
        if int(rating) not in range(1,6):
            messages.error(request, "امتیاز نامعتبر است.")
            return redirect("product_detail", pk=pk)

        Comment.objects.create(user=request.user, product=product, text=text, rating=int(rating),)
        messages.success(request, "نظر شما با موفقیت ثبت شد.")

    return redirect("product_detail", pk=pk)


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    product_id = comment.product.id

    comment.delete()
    messages.success(request, "نظر حذف شد.")

    return redirect("product_detail", pk=product_id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == "POST":
        comment.text = request.POST["text"]
        comment.rating = request.POST["rating"]

        comment.save()
        messages.success(request, "نظر ویرایش شد.")

        return redirect("product_detail", pk=comment.product.id)

    return render(request, "edit_comment.html", {"comment": comment})