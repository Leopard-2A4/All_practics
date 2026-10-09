from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (ShopIndexView, ProductsListView,
                    OrdersListView, CreateProductView,
                    CreateOrderView, DeleteOrderView,
                    DeleteProductView, OrdersDetailView,
                    ProductsDetailView, UpdateProductView,
                    UpdateOrderView, OrdersDataExportView,
                    ProductViewSet, OrderViewSet,
                    LatestProductsFeed, UserOrdersListView,
                    UserOrdersDataExportView)

app_name = 'shopapp'

router_products = DefaultRouter()
router_products.register("products", ProductViewSet)

router_orders = DefaultRouter()
router_orders.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/products/", include(router_products.urls)),
    path("api/orders/", include(router_orders.urls)),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("products/create_product/", CreateProductView.as_view(), name="create_product"),
    path("orders/create_order/", CreateOrderView.as_view(), name="create_order"),
    path("orders/<int:pk>/delete_order/", DeleteOrderView.as_view(), name="delete_order"),
    path("products/<int:pk>/delete_product/", DeleteProductView.as_view(), name="delete_product"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="details_order"),
    path("products/<int:pk>/", ProductsDetailView.as_view(), name="details_product"),
    path("orders/<int:pk>/update_order/", UpdateOrderView.as_view(), name="update_order"),
    path("products/<int:pk>/update_product/", UpdateProductView.as_view(), name="update_product"),
    path("orders/export", OrdersDataExportView.as_view(), name="orders-export"),
    path("products/latest/feed/", LatestProductsFeed(), name="latest_products_feed"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user-orders"),
    path("users/<int:user_id>/orders/export/", UserOrdersDataExportView.as_view(), name="user-orders-export"),
]
