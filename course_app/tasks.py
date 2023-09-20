from datetime import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import pytz

from users.models import User


@shared_task
def message_update_course(email):
    """Отправляет сообщение об обновлении курса подписчикам курса"""
    # Код задачи
    send_mail(
        subject='Курс обновился!',
        message=f'Зайдите и Посмотрите, что нового в вашем курсе',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email,
        fail_silently=False,
    )


@shared_task()
def blocking_user():
    timezone = pytz.timezone('Europe/Moscow')
    users = User.objects.all()
    for user in users:
        if user.last_login:
            diff = datetime.now(timezone) - user.last_login

            if diff and diff.days >= 30:
                user.is_active = False
                user.save()
