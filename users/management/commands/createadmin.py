from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = os.getenv('EMAIL')

        # Проверяем, нет ли уже такого пользователя
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_superuser(
                email=email,
                first_name=os.getenv('FIRST_NAME'),
                last_name=os.getenv('LAST_NAME'),
                password=os.getenv('PASSWORD_ADMIN')
            )
            self.stdout.write(self.style.SUCCESS(f'Админ {user.email} создан!'))
        else:
            self.stdout.write(self.style.WARNING(f'Админ {email} уже существует.'))
