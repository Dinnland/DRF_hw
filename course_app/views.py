import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response

from course_app.models import Course, Lesson, Payment, Subscription
from course_app.paginators import CourseAppPaginator
from course_app.permissions import IsOwnerOrStaffOrModerator, IsNotModerator, ModeratorPermission, IsOwner
from course_app.serializers.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    SubscriptionSerializer, PaymentCreateSerializer, PaymentRetrieveSerializer
from course_app.services import retrieve_session, get_session, get_emails
from course_app.tasks import message_update_course


# Course -------------------------------------------------------------------------------------------------------------


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

    def update(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(user=request.user)
        print(subscriptions)
        emails = get_emails(subscriptions)
        print(emails)

        message_update_course.delay(emails)
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        upd_course = serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


# Lesson -----------------------------------------------------------------------------------------------------------


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
        # print(my_task.delay(1))
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


# Payment -----------------------------------------------------------------------------------------------------------


class PaymentListAPIView(generics.ListAPIView):
    """ Получаем список Payment"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_type'
    filterset_fields = ('course', 'lesson', 'payment_type')
    # сортировка по дате оплаты
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создаем платеж - Payment"""
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get('lesson')
        course = serializer.validated_data.get('course')
        if not lesson and not course:
            raise serializers.ValidationError({
                'non_empty_fields': 'Заполните поле: lesson или course'
            })
        new_pay = serializer.save()
        new_pay.user = self.request.user
        new_pay.session = get_session(new_pay).id
        new_pay.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Получаем список Payment"""
    serializer_class = PaymentRetrieveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        session = retrieve_session(obj.session)
        if session.payment_status == 'paid' and session.status == 'complete':
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj

# Subscription ---------------------------------------------------------------------------------------------------------


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

        new_subscription.user = self.request.user
        # new_subscription.Course = self.kwargs["pk"]

        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 по pk"""
    queryset = Subscription.objects.all()


# STRIPE - оплата --------------------------------------------------------------------------------------------------

#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
# class CreateCheckoutSessionView(View):
#
#
#
#     def post(self, request, *args, **kwargs):
#
#         payment_id = self.kwargs["pk"]
#         payment = Payment.objects.get(id=payment_id)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         payment_name = payment.user + payment.date_of_payment
#         checkout_session = stripe.checkout.Session.create(
#             # тут наверное надо иф
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'rub',
#                         'unit_amount': payment.payment_amount,
#                         'product_data': {
#                             # можно подумать конечно
#                             'name': payment_name
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": payment.id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#             # надеюсь сработает
#             customer_email=Payment.user,
#         )
#         # хмммммммммм
#         return JsonResponse({
#             'id': checkout_session.id
#         })
