from django.shortcuts import get_object_or_404, redirect
from .models import Product, Category, Brand, Wishlist, Comment
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import *

# Create your views here.

class HomeView(TemplateView):
    template_name="home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context["latest_products"]=Product.objects.filter(is_active=True).order_by("-created_at")[:8]
        context["categories"]=Category.objects.all()
        context["brands"]=Brand.objects.all()[:8]

        return context


class ProductListView(ListView):
    model=Product
    template_name="product_list.html"
    context_object_name = "products"
    paginate_by=6

    def get_queryset(self):
        queryset=Product.objects.filter(is_active=True).order_by("-created_at")
        category=self.request.GET.get("category")
        brand=self.request.GET.get("brand")
        sort=self.request.GET.get("sort")
        q=self.request.GET.get("q")

        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        
        if category:
            queryset=queryset.filter(category__slug=category)
        
        if brand:
            queryset=queryset.filter(brand__slug=brand)
        
        if sort=="price_low":
            queryset=queryset.order_by("price")

        if sort=="price_high":
            queryset=queryset.order_by("-price")

        return queryset
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context["categories"]=Category.objects.all()
        context["brands"]=Brand.objects.all()
        context["selected_category"]=self.request.GET.get("category")
        context["selected_sort"]=self.request.GET.get("sort")
        context["q"]=self.request.GET.get("q")

        return context


class ProductDetailView(DetailView):
    model=Product
    template_name="product_detail.html"
    context_object_name="product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        product=self.object
        approved_comments=product.comments.filter(is_approved=True)

        context["avg_rating"]=(approved_comments.aggregate(Avg("rating"))["rating__avg"])
        context["comment_count"]=(approved_comments.count())
        paginator=Paginator(approved_comments.order_by("-created_at"), 5)
        page_number = self.request.GET.get("comment_page")
        context["comments"] = (paginator.get_page(page_number))
        context["images"] = (product.images.all())
        context["main_image"] = (product.image)
        context["in_wishlist"] = False
        context["user_has_commented"] = False

        if self.request.user.is_authenticated:

            context["in_wishlist"] = (Wishlist.objects.filter(user=self.request.user, product=product).exists())

            context["user_has_commented"] = (Comment.objects.filter(user=self.request.user, product=product).exists())

        return context

class AjaxSearchProductsView(View):

    def get(self, request):

        query = request.GET.get("q", "")

        products = Product.objects.filter(name__icontains=query, is_active=True)[:10]

        data = []

        for product in products:

            data.append({"id": product.id, "name": product.name, "price": str(product.price), "brand": product.brand.name, "image": (
                    product.image.url if product.image else "/static/images/no-image.jpg"),})

        return JsonResponse(data, safe=False)


class ToggleWishList(LoginRequiredMixin, View):
    def post(self, request, pk):
        product=get_object_or_404(Product, pk=pk)

        wishlist_item, created=(Wishlist.objects.get_or_create(user=request.user, product=product))

        if created:
            in_wishlist=True
        else:
            wishlist_item.delete()
            in_wishlist=False
        
        wishlist_count = (Wishlist.objects.filter(user=request.user).count())

        return JsonResponse({"success": True, "in_wishlist": in_wishlist, "wishlist_count": wishlist_count,})


class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return (Wishlist.objects.filter(user=self.request.user).select_related("product"))


class AddCommentView(LoginRequiredMixin, CreateView):
    model=Comment
    form_class=CommentForm

    def form_valid(self, form):
        product=get_object_or_404(Product, pk=self.kwargs["pk"], is_active=True)
        form.instance.user=self.request.user
        form.instance.product=product

        if Comment.objects.filter(user=self.request.user, product=product).exists():

            messages.warning(self.request, "قبلاً نظر ثبت کرده‌اید.")

            return redirect("product_detail", pk=product.pk)

        return super().form_valid(form)
    
    def get_success_url(self):

        return reverse("product_detail", kwargs={"pk": self.object.product.pk})
    
    
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"

    def get_queryset(self):

        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):

        return reverse("product_detail", kwargs={"pk": self.object.product.pk})

class EditCommentView(LoginRequiredMixin, UpdateView):
    
    model = Comment
    form_class = CommentForm
    template_name = "edit_comment.html"
    pk_url_kwarg = "comment_id"

    def get_queryset(self):

        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):

        return reverse("product_detail", kwargs={"pk": self.object.product.pk})