from django.contrib.auth.models import User, Permission
from django.test import TestCase
from shopapp.models import Order
from django.shortcuts import reverse


# Create your tests here.
class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            username="testuser",
            password="qwerty"
        )

        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

        self.order = Order.objects.create(
            delivery_address="Example street",
            promocode="promex",
            user=self.user,
        )

    def tearDown(self):
        self.order.delete()

    def test_order_detail_view(self):
        response = self.client.get(
            reverse(
                "shopapp:details_order",
                kwargs={"pk": self.order.pk},
            )
        )

        self.assertContains(response, "Example street")
        self.assertContains(response, "promex")

        self.assertEqual(
            self.order.pk,
            response.context["order"].pk,
        )

class OrdersExportTestCase(TestCase):

    fixtures = ["orders-fixture.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            username="testuser",
            password="qwerty",
            is_staff=True,
            is_active=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_export_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export")
        )

        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by("pk")

        expected_data = [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products": list(
                    order.products.values_list("pk", flat=True)
                ),
            }
            for order in orders
        ]

        orders_data = response.json()

        self.assertEqual(
            orders_data["orders"],
            expected_data
        )