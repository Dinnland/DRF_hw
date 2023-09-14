from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from course_app.models import Course, Lesson, Payment, Subscription
from course_app.paginators import CourseAppPaginator
from course_app.permissions import IsOwnerOrStaffOrModerator, IsNotModerator, ModeratorPermission, IsOwner
from course_app.serializers.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    SubscriptionSerializer


# КУРС -------------------------------------------------------------------------------------------------------------


class CourseViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для Course """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [ModeratorPermission]
    pagination_class = CourseAppPaginator

    def get_permissions(self):
        """
        Instantiates and returns the list,destroy of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsNotModerator]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrStaffOrModerator]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            print('.request.user.groups.filter(name="moderator").exists():')
            return Course.objects.all()
        print(self.request.user)

        return Course.objects.filter(owner=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        upd_course = serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


# УРОКИ -----------------------------------------------------------------------------------------------------------


class LessonCreateAPIView(generics.CreateAPIView):
    """Создаем урок (Lesson)"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]  # work
    # permission_classes = [IsAuthenticated, ModeratorPermission]  # err get_queryset, queryset
    # permission_classes = [AllowAny]
    def perform_create(self, serializer):
        # автоматом пользователь, создавая урок, становится владельцем
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='moderator').exists():
    #         return Course.objects.all()
    #     print(self.request.user)
    #
    #     return Course.objects.filter(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Получаем список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffOrModerator]  # work
    # permission_classes = [ModeratorPermission]
    pagination_class = CourseAppPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermission]  # work


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновляем 1 урок по pk"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermission]  # work


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 урок по pk"""
    # serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]  # work


# ПЛАТЕЖ -----------------------------------------------------------------------------------------------------------


class PaymentListAPIView(generics.ListAPIView):
    """ Получаем список Payment"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_type'
    filterset_fields = ('course', 'lesson', 'payment_type')
    # сортировка по дате оплаты
    ordering_fields = ('date_of_payment',)


# ПОДПИСКА ---------------------------------------------------------------------------------------------------------


class SubscriptionListAPIView(generics.ListAPIView):
    """Получаем список уроков"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated] # work
    # permission_classes = [ModeratorPermission]
    # pagination_class = CourseAppPaginator

    def get_queryset(self):
        # if self.request.user.groups.filter(name='moderator').exists():
        #     return Lesson.objects.all()
        # return Lesson.objects.filter(owner=self.request.user)
        return Subscription.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Создаем подписку (Subscription)"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsNotModerator]
    # queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        # автоматом пользователь, создавая подписку, становится владельцем
        new_subscription = serializer.save()
        # print(F'HUI====={self.request.user}'
        #       F'PIZDA===={self.kwargs["pk"]}')
        new_subscription.user = self.request.user
        new_subscription.Course = self.kwargs["pk"]

        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 по pk"""
    queryset = Subscription.objects.all()
