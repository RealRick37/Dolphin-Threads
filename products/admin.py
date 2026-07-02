from django.contrib import admin
from .models import *
# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Wishlist)
admin.site.register(Comment)
admin.site.register(ProductImage)