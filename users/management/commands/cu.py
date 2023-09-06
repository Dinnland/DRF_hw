from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создание учетных записей обычных пользователей"""
        # 1
        user = User.objects.create(
            email='test1@test.ru',
            phone='1234567890',
            city='Kazan',

        )
        user.set_password('1111')
        user.save()

        # 2
        user = User.objects.create(
            email='test2@test.ru',
            phone='89176666666',
            city='Detroit',
            country='USA',
        )
        user.set_password('2222')
        user.save()
