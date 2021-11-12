from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            User(
                username=f"test_user{index}",
                email=f"test_mail{index}@mail.com",
                password=make_password(f"test_password{index}"),
                is_staff=True,
                is_superuser=True,
            )
            for index in range(1, 4)
        ]
        User.objects.bulk_create(users)
        return "Successfully created users."
