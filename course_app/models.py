from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """Курс"""
    name = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course_app/course', verbose_name='превью (изображение)', **NULLABLE)
    description = models.TextField(verbose_name='описание')

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

    # def __int__(self):
    #     return f'{self.email} {self.name} {self.surname}'

    def __str__(self):
        return f'{self.name} '

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('name',)
