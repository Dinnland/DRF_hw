from rest_framework import viewsets, generics

from course_app.models import Course, Lesson
from course_app.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для Course """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создаем урок (Lesson)"""
    serializer_class = LessonSerializer
    # queryset = Lesson.objects.all()


class LessonListAPIView(generics.ListAPIView):
    """Получаем список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Получаем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 урок по pk"""
    # serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

