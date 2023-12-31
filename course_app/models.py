from django.db import models

from drf_din import settings
from users.models import User
from django.utils.timezone import now

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """Курс"""
    name = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course_app/course', verbose_name='превью (изображение)', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Создатель')
    # owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    # def __int__(self):
    #     return f'{self.email} {self.name} {self.surname}'

    def __str__(self):
        return f'{self.name} '

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('name',)


class Lesson(models.Model):
    """Урок"""
    name = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course_app/lesson', verbose_name='превью (изображение)', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video_url = models.CharField(max_length=300, verbose_name='ссылка на видео', **NULLABLE)

    course = models.ForeignKey('Course', on_delete=models.SET_NULL,
                               verbose_name='ссылка на курс', related_name='lessons', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Создатель')
    # def __int__(self):
    #     return f'{self.email} {self.name} {self.surname}'

    def __str__(self):
        return f'{self.name} '

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('name',)


class Payment(models.Model):
    """Платеж"""
    PAYMENT_TYPE = (
        ('cash', 'наличные'),
        ('transfer', 'перевод на счет')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='the_user')
    date_of_payment = models.DateTimeField(default=now)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='оплаченный курс',
                               related_name='courses', **NULLABLE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='оплаченный урок',
                               related_name='lessons', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE, verbose_name='способ оплаты')

    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')
    session = models.CharField(max_length=180, verbose_name='сессия для оплаты', **NULLABLE)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)


class Subscription(models.Model):
    """Подписка"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
