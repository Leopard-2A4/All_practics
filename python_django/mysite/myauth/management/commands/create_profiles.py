from django.contrib.auth.models import User
from django.core.management import BaseCommand

from myauth.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start creating profiles...")

        users = User.objects.filter(id__in=[1, 3])

        for user in users:
            profile, created = Profile.objects.get_or_create(
                user=user
            )

            if not created:
                self.stdout.write(
                    self.style.WARNING(
                        f"Profile already exists for {user.username}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created profile for {user.username}"
                    )
                )