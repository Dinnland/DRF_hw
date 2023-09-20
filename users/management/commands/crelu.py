from django.core.management import BaseCommand

from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создание учетных записей реальных пользователей"""
        # 1
        user = User.objects.create(
            email='dinarek2013@gmail.com',

        )
        user.set_password('2222')
        user.save()
