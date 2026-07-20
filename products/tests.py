from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Product, Category, Brand

# Create your tests here.

class ProductAPITest(APITestCase):
    def setUp(self):
        category=Category.objects.create(name="Tshirts", slug="tshirts")
        brand=Brand.objects.create(name="Nike", slug="nike")
        Product.objects.create(name="Test Product", description="Test", category=category, brand=brand, price=100)

    def test_product_list(self):
        url=reverse("product-list")
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)