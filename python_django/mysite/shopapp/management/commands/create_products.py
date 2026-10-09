from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start creating products...")
        list_of_new_products = [
            "apple",
            "banana",
            "Orange"
        ]
        for product in list_of_new_products:
            product, created = Product.objects.get_or_create(name=product)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Product {product.name} is already in DB"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Product {product.name} now in DB"))
        self.stdout.write(
            self.style.SUCCESS("Now products in DB"))
