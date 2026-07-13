from django.urls import path
from .api_views import ProductListAPIView, ProductDetailAPIView, ProducCreateAPIView, ProductUpdateAPIView, ProductDeleteAPIView

urlpatterns=[
    path("products/", ProductListAPIView.as_view(), name="api_products"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="api_product_detail "),
    path("products/<int:pk>/update/", ProductUpdateAPIView.as_view(), name="api_product_update "),
    path("products/<int:pk>/delete/", ProductDeleteAPIView.as_view(), name="api_product_delete "),
    path("products/create/", ProducCreateAPIView.as_view(), name="api_product_create "),
]