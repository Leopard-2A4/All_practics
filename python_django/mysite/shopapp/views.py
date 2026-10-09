from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        UserPassesTestMixin, LoginRequiredMixin)
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.syndication.views import Feed
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView)
from rest_framework.renderers import JSONRenderer

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

# Create your views here.

class UserOrdersDataExportView(View):

    def get(self, request: HttpRequest, user_id: int):
        self.c_key = f"test_key{user_id}"
        self.owner = User.objects.get(pk=self.kwargs["user_id"])
        orders = Order.objects.filter(user=self.owner)

        orders_data = cache.get(self.c_key)
        if orders_data is None:
            orders_data = OrderSerializer(orders, many=True).data
            cache.set(self.c_key, orders_data, 120)

        return HttpResponse(orders_data,
                            content_type="application/json")

class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/user-orders-list.html"
    context_object_name = "orders"

    def get_queryset(self):
        self.owner = User.objects.get(pk=self.kwargs["user_id"])
        return Order.objects.filter(user=self.owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.owner
        return context

class LatestProductsFeed(Feed):
    title = "New Products"
    description = "Changes by add new Products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (Product.objects.order_by("-created_at")[:5])

    def item_title(self, item: Product):
        return item.name

    def item_link(self, item: Product):
        return reverse("shopapp:details_product", kwargs={"pk": item.pk})

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter, OrderingFilter
    ]
    search_fields = ["name"]
    ordering_fields = ["name"]
    filterset_fields = ["name", "description", "price"]

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        OrderingFilter, DjangoFilterBackend
    ]
    ordering_fields = ["user", "delivery_address"]
    filterset_fields = ["delivery_address", "user", "promocode"]

class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ("appLe", 2.89),
            ("baNana", 3.99),
            ("Oranges", 6.78),
        ]
        context = {
            "Some_text": "We best shop in the world !",
            "products": products,
        }
        return render(request, "shopapp/shop-index.html", context)

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"

class ProductsDetailView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.filter(archived=False)
    context_object_name = "product"

class OrdersListView(ListView):
    template_name = "shopapp/orders-list.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = "orders"

class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    template_name = "shopapp/orders-details.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = "order"

class CreateProductView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    template_name = "shopapp/create-product.html"
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateProductView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        user = self.request.user
        return user.is_superuser or (
                user.has_perm("shopapp.change_product")
                and self.object.created_by == user
        )

    template_name = "shopapp/product-update.html"
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

class DeleteProductView(DeleteView):
    template_name = "shopapp/product-delete.html"
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

class CreateOrderView(CreateView):
    template_name = "shopapp/create-order.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    fields = "user", "delivery_address", "promocode", "products"
    success_url = reverse_lazy("shopapp:orders_list")

class UpdateOrderView(UpdateView):
    template_name = "shopapp/order-update.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    fields = "user", "delivery_address", "promocode", "products"
    success_url = reverse_lazy("shopapp:orders_list")

class DeleteOrderView(DeleteView):
    template_name = "shopapp/order-delete.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    success_url = reverse_lazy("shopapp:orders_list")

class OrdersDataExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest):
        orders = Order.objects.order_by("pk")

        orders_data = [
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

        return JsonResponse({"orders": orders_data})