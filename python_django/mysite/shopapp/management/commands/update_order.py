from django.core.management import BaseCommand
from shopapp.models import Product, Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.all()
        if not order:
            self.stdout.write(self.style.ERROR("No orders found"))
            return
        products = Product.objects.all()

        for product in products:
            order.product.add(product)

        order.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added products: {order.products.all()} "
                f", to order {order}")
        )