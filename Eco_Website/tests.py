import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.exceptions import ValidationError
from .models import Category, Customer, Product, Order
from .views import home, about


class CategoryModelTest(TestCase):
    """Unit tests for Category model (Positive, Negative, Edge Cases)"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation_positive(self):
        """Test creating a category with valid parameters."""
        self.assertEqual(self.category.name, "Electronics")
        self.assertTrue(isinstance(self.category, Category))

    def test_category_str_representation(self):
        """Test __str__ method returns category name."""
        self.assertEqual(str(self.category), "Electronics")

    def test_category_verbose_name_plural(self):
        """Test Meta option verbose_name_plural is correctly set to 'Categories'."""
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")

    def test_category_max_length_validation(self):
        """Test ValidationError is raised when category name exceeds 50 characters."""
        long_name = "A" * 51
        category = Category(name=long_name)
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_update(self):
        """Test updating category fields."""
        self.category.name = "Smart Gadgets"
        self.category.save()
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, "Smart Gadgets")

    def test_category_deletion(self):
        """Test deleting a category."""
        category_id = self.category.id
        self.category.delete()
        self.assertFalse(Category.objects.filter(id=category_id).exists())


class CustomerModelTest(TestCase):
    """Unit tests for Customer model (Positive, Negative, Edge Cases)"""

    def setUp(self):
        self.customer_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St, Tech City",
            "phone": "1234567890",
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_customer_creation_positive(self):
        """Test customer creation with valid fields."""
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "john.doe@example.com")
        self.assertEqual(self.customer.address, "123 Main St, Tech City")
        self.assertEqual(self.customer.phone, "1234567890")

    def test_customer_str_representation(self):
        """Test __str__ method returns formatted string with spaces."""
        self.assertEqual(str(self.customer), " John Doe ")

    def test_customer_invalid_email_validation(self):
        """Test validation fails when email format is invalid."""
        invalid_customer = Customer(
            name="Jane Doe",
            email="not-an-email",
            address="456 Elm St",
            phone="0987654321",
        )
        with self.assertRaises(ValidationError):
            invalid_customer.full_clean()

    def test_customer_max_length_exceeded(self):
        """Test validation fails when name exceeds 50 characters."""
        overlong_customer = Customer(
            name="X" * 51,
            email="valid@example.com",
            address="123 Street",
            phone="123",
        )
        with self.assertRaises(ValidationError):
            overlong_customer.full_clean()


class ProductModelTest(TestCase):
    """Unit tests for Product model (Positive, Negative, Edge Cases)"""

    def setUp(self):
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Python Basics",
            price=29.99,
            Category=self.category,
            image="uploads/product/python.jpg",
        )

    def test_product_creation_positive(self):
        """Test creation of product with default flags and values."""
        self.assertEqual(self.product.name, "Python Basics")
        self.assertEqual(self.product.price, 29.99)
        self.assertEqual(self.product.Category, self.category)
        self.assertFalse(self.product.is_sale)
        self.assertEqual(self.product.sale_price, Decimal("0.00"))

    def test_product_str_representation(self):
        """Test __str__ method returns formatted product name with spaces."""
        self.assertEqual(str(self.product), " Python Basics ")

    def test_product_on_sale_creation(self):
        """Test creating a product on sale with custom sale price."""
        sale_product = Product.objects.create(
            name="Discounted Novel",
            price=19.99,
            Category=self.category,
            image="uploads/product/novel.jpg",
            is_sale=True,
            sale_price=Decimal("14.99"),
        )
        self.assertTrue(sale_product.is_sale)
        self.assertEqual(sale_product.sale_price, Decimal("14.99"))

    def test_product_cascade_on_category_delete(self):
        """Test that deleting a category cascades and deletes associated products."""
        product_id = self.product.id
        self.category.delete()
        self.assertFalse(Product.objects.filter(id=product_id).exists())


class OrderModelTest(TestCase):
    """Unit tests for Order model (Positive, Negative, Edge Cases)"""

    def setUp(self):
        self.category = Category.objects.create(name="Home")
        self.product = Product.objects.create(
            name="Lamp",
            price=15.50,
            Category=self.category,
            image="uploads/product/lamp.jpg",
        )
        self.customer = Customer.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            address="789 Pine St",
            phone="5551234",
        )

    def test_order_creation_defaults(self):
        """Test order creation with default values for quantity, status, date, phone, and address."""
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
        )
        self.assertEqual(order.quantity, 1)
        self.assertEqual(order.phone, "")
        self.assertEqual(order.address, "")
        self.assertFalse(order.status)
        self.assertEqual(order.data, datetime.date.today())

    def test_order_creation_custom_values(self):
        """Test order creation with non-default values."""
        custom_date = datetime.date(2025, 1, 1)
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=5,
            phone="9998887777",
            address="100 Custom Road",
            status=True,
            data=custom_date,
        )
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.phone, "9998887777")
        self.assertEqual(order.address, "100 Custom Road")
        self.assertTrue(order.status)
        self.assertEqual(order.data, custom_date)

    def test_order_str_representation(self):
        """Test __str__ method returns string representation of linked product."""
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
        )
        self.assertEqual(str(order), str(self.product))

    def test_order_cascade_on_product_delete(self):
        """Test that deleting the product deletes the associated order."""
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
        )
        order_id = order.id
        self.product.delete()
        self.assertFalse(Order.objects.filter(id=order_id).exists())

    def test_order_cascade_on_customer_delete(self):
        """Test that deleting the customer deletes the associated order."""
        order = Order.objects.create(
            product=self.product,
            customer=self.customer,
        )
        order_id = order.id
        self.customer.delete()
        self.assertFalse(Order.objects.filter(id=order_id).exists())


class ViewsAndUrlsTest(TestCase):
    """Unit tests for Views, Contexts, Templates, and Routing."""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="General")

    def test_home_url_resolves_to_home_view(self):
        """Test home URL pattern name resolves to home function."""
        resolver = resolve("/")
        self.assertEqual(resolver.func, home)

    def test_about_url_resolves_to_about_view(self):
        """Test about URL pattern name resolves to about function."""
        resolver = resolve("/about/")
        self.assertEqual(resolver.func, about)

    def test_home_view_status_code_and_template(self):
        """Test home view returns 200 OK status code and uses correct template."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_about_view_status_code_and_template(self):
        """Test about view returns 200 OK status code and uses correct template."""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_home_view_context_empty_products(self):
        """Test home view context when no products exist in database."""
        response = self.client.get(reverse("home"))
        self.assertIn("products", response.context)
        self.assertEqual(len(response.context["products"]), 0)

    def test_home_view_context_with_products(self):
        """Test home view context returns list of products."""
        prod1 = Product.objects.create(
            name="Prod 1", price=10.0, Category=self.category, image="p1.jpg"
        )
        prod2 = Product.objects.create(
            name="Prod 2", price=20.0, Category=self.category, image="p2.jpg"
        )
        response = self.client.get(reverse("home"))
        self.assertIn("products", response.context)
        products = response.context["products"]
        self.assertEqual(len(products), 2)
        self.assertIn(prod1, products)
        self.assertIn(prod2, products)

