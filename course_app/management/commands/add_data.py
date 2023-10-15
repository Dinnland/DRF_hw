from django.core.management import BaseCommand

from course_app.models import Course, Lesson, Payment
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Очистка бд, кроме админа
        for u in User.objects.all():
            if not u.is_superuser:
                u.delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        # создание юзеров
        user1 = User.objects.create(email='user1@example.com', phone='1234567890', city='Kazan')
        user1.set_password('1111')
        user1.save()

        user2 = User.objects.create(email='user2@example.com', phone='89176666666', city='Detroit', country='USA')
        user2.set_password('2222')
        user2.save()

        # создание курсов
        course_name1 = 'Course 1'
        course_name2 = 'Course 2'
        # for i in Course.objects.all():
            # print(i.name )
            #
            # if i.name == 'Course 1':
            #     course_name1 = 'Course 111111111111111'
            #
            # if i.name == 'Course 2':
            #     course_name2 = 'Course 222222222222222'

        course1 = Course.objects.create(name=course_name1, description='Description 1')
        course2 = Course.objects.create(name=course_name2, description='Description 2')

        # создание уроков
        lesson1 = Lesson.objects.create(name='Lesson 1', description='Lesson Description 1', video_url='https://example.com/video1', course=course1)
        lesson2 = Lesson.objects.create(name='Lesson 2', description='Lesson Description 2', video_url='https://example.com/video2', course=course2)

        # создание оплаты
        payment1 = Payment.objects.create(user=user1, course=course1, lesson=lesson1, payment_amount=999.0, payment_type='cash')
        payment2 = Payment.objects.create(user=user2, course=course2, lesson=lesson2, payment_amount=555.0, payment_type='transfer')
