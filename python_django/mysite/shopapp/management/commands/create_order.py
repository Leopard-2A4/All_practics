from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product, Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start creating orders...")
        user = User.objects.get(username="user")
        order, created = Order.objects.get_or_create(
            delivery_address="st. Kalinina / house: 3 / corp.3",
            promocode="G-36",
            user=user,
        )
        if not created:
            self.stdout.write(
                self.style.WARNING(f"Order already created, order: {order}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Created order: {order}")
            )
