from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name=models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to="products/", blank=True, null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    class Meta:
        unique_together=("product", "color", "size")
        
    SIZE_CHOICES=[
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("ّFree Size", "ّFree Size"),
        ("ّ38-44", "ّ38-44"),
        ("ّ-", "ّ-"),
    ]
    
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color=models.ForeignKey(Color, on_delete=models.CASCADE, related_name="variants")
    size=models.CharField(max_length=10, choices=SIZE_CHOICES)
    stock=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size}"
    

class Wishlist(models.Model):
    user=models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="wishlist_items")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("user", "product")

class Comment(models.Model):
    user=models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_approved=models.BooleanField(default=True)

    rating=models.IntegerField(
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ]
    )

    def __str__(self):
        return f"{self.user.username} commented on {self.product.name}"
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=150, blank=True)
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} image"