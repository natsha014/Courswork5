from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = os.getenv('EMAIL')

        User.objects.filter(email=email).delete()

        user = User.objects.create(
            email=email,
            first_name=os.getenv('FIRST_NAME'),
            last_name=os.getenv('LAST_NAME'),
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(os.getenv('PASSWORD_ADMIN'))
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {user.email}'))
