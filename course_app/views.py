from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course_app.models import Course, Lesson, Payment
from course_app.permissions import *
from course_app.serializers.serializers import CourseSerializer, LessonSerializer, CourseListSerializer, \
    PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для Course """
    # serializer_class = CourseSerializer
    serializer_class = CourseListSerializer

    queryset = Course.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list,destroy of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsNotModerator]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        print(self.request.user)

        return Course.objects.filter(owner=self.request.user)


    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        upd_course = serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создаем урок (Lesson)"""
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsNotModerator]
    def perform_create(self, serializer):
        # автоматом пользователь, создавая урок, становится владельцем
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Получаем список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffOrModeratorQWERTY]

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновляем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 урок по pk"""
    # serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


# платежи


class PaymentListAPIView(generics.ListAPIView):
    """ Получаем список Payment"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_type'
    filterset_fields = ('course', 'lesson', 'payment_type')
    # сортировка по дате оплаты
    ordering_fields = ('date_of_payment',)
