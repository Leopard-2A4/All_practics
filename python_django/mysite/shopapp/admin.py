from csv import DictReader
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import path

from .forms import CSVImportForm
from io import TextIOWrapper
from .models import Product, Order
# Register your models here.

class ProductInline(admin.StackedInline):
    model = Order.products.through


class OrdersInline(admin.StackedInline):
    model = Product.orders.through

@admin.action(description="'Archive products")
def archive(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="'Unarchive products")
def unarchive(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        OrdersInline,
    ]
    list_display = "pk", "name", "description_short", "price", "archived"
    list_display_links = "pk", "name"
    ordering = "pk", "name", "price"
    searching_fields = "name", "description", "price"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Other", {
            "fields": ("archived",),
            "classes": ("wide", "collapse"),
        })
    ]
    actions = [archive, unarchive]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return obj.description[:48] + "..."
        return obj.description


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/orders_changelist.html"
    inline = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.username or obj.user.first_name

    def import_csv(self, request: HttpRequest):
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv-form.html", context=context)

        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(
                request,
                "admin/csv-form.html",
                context=context,
                status=400,
            )

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )

        reader = DictReader(csv_file)

        for row in reader:
            product_ids = row.pop("products").split(";")

            row["user_id"] = row.pop("user")

            order = Order.objects.create(**row)

            order.products.set(product_ids)

        self.message_user(
            request,
            "Data from CSV has imported"
        )

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-orders-csv/",
                 self.import_csv,
                 name="upload_orders_csv",
            ),
        ]
        return new_urls + urls