from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant, Category, Brand, Color

# Create your tests here.

User = get_user_model()

class CartAPITest(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="kivy",password="kivy123456!")
        category=Category.objects.create(name="Tshirts", slug="tshirts")
        brand=Brand.objects.create(name="Nike", slug="nike")
        color=Color.objects.create(name="Black")

        product=Product.objects.create(name="Shirt", description="Test", category=category, brand=brand, price=100)
        self.variant=ProductVariant.objects.create(product=product, color=color, size="L",stock=10)

    def test_add_to_cart(self):
        self.client.force_authenticate(self.user)
        url=reverse("api_add_to_cart")
        response=self.client.post(url, {"variant_id": self.variant.id, "quantity": 2})
        self.assertEqual(response.status_code, 201)